# -*- coding: utf-8 -*-

# Python argparse 命令行参数解析 完整示例

import argparse


# ====================== 1. 基础用法：创建解析器 + 位置参数 ======================
def demo_basic():
    parser = argparse.ArgumentParser(description="基础示例：位置参数")
    parser.add_argument("name", help="你的名字")
    parser.add_argument("age", type=int, help="你的年龄")
    args = parser.parse_args(["Alice", "25"])
    print(f"名字: {args.name}, 年龄: {args.age}")


# ====================== 2. 可选参数 / 标志 ======================
def demo_optional():
    parser = argparse.ArgumentParser(description="可选参数示例")
    parser.add_argument("--name", "-n", default="World", help="名字（默认: World）")
    parser.add_argument("--verbose", "-v", action="store_true", help="是否输出详细信息")
    args = parser.parse_args(["--name", "Tom", "-v"])
    if args.verbose:
        print(f"详细信息: Hello, {args.name}!")
    else:
        print(f"Hello, {args.name}")


# ====================== 3. 类型转换 (type) ======================
def demo_type():
    parser = argparse.ArgumentParser(description="类型转换示例")
    parser.add_argument("--count", type=int, default=1, help="重复次数 (int)")
    parser.add_argument("--rate", type=float, default=1.0, help="倍率 (float)")
    parser.add_argument("--items", type=int, nargs="+", help="多个整数")
    args = parser.parse_args(["--count", "3", "--rate", "2.5", "--items", "10", "20", "30"])
    total = sum(args.items) * args.rate
    print(f"count={args.count}, rate={args.rate}, items={args.items}, 加权总和={total}")


# ====================== 4. choices 限定可选值 ======================
def demo_choices():
    parser = argparse.ArgumentParser(description="choices 限定可选值")
    parser.add_argument("--color", choices=["red", "green", "blue"], required=True, help="颜色")
    parser.add_argument("--size", choices=["S", "M", "L", "XL"], default="M", help="尺寸")
    args = parser.parse_args(["--color", "red", "--size", "L"])
    print(f"选择的颜色: {args.color}, 尺寸: {args.size}")


# ====================== 5. action 动作类型 ======================
def demo_action():
    parser = argparse.ArgumentParser(description="action 动作类型示例")

    # store_true: 出现即为 True，不出现为 False
    parser.add_argument("--debug", action="store_true", help="开启调试模式")

    # store_false: 出现即为 False，不出现为 True
    parser.add_argument("--no-cache", action="store_false", dest="cache", help="禁用缓存")

    # count: 统计出现次数 (-v → 1, -vv → 2, -vvv → 3)
    parser.add_argument("-v", "--verbose", action="count", default=0, help="冗长级别")

    # append: 每次出现追加到列表
    parser.add_argument("--tag", action="append", default=[], help="标签（可多次指定）")

    args = parser.parse_args(["--debug", "--no-cache", "-vvv", "--tag", "python", "--tag", "argparse"])
    print(f"debug={args.debug}, cache={args.cache}, verbose={args.verbose}, tags={args.tag}")


# ====================== 6. nargs 参数数量 ======================
def demo_nargs():
    parser = argparse.ArgumentParser(description="nargs 参数数量示例")

    # N: 固定数量
    parser.add_argument("--point", nargs=2, type=int, help="坐标点 x y")

    # ?: 0或1个
    parser.add_argument("--log", nargs="?", const="app.log", default=None, help="日志文件")

    # *: 0个或多个
    parser.add_argument("files", nargs="*", default=[], help="文件列表")

    # +: 1个或多个
    parser.add_argument("--ports", nargs="+", type=int, help="端口列表")

    # 分开演示以避免 nargs="+" 与 nargs="*" 之间的贪婪冲突
    args1 = parser.parse_args(["--point", "100", "200", "--ports", "8080", "9090", "--log"])
    print(f"[演示1] point={args1.point}, ports={args1.ports}, log={args1.log}, files={args1.files}")

    args2 = parser.parse_args(["a.txt", "b.txt"])
    print(f"[演示2] files={args2.files}")


# ====================== 7. 互斥组 (mutually exclusive group) ======================
def demo_mutually_exclusive():
    parser = argparse.ArgumentParser(description="互斥组示例")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start", action="store_true", help="启动服务")
    group.add_argument("--stop", action="store_true", help="停止服务")
    group.add_argument("--restart", action="store_true", help="重启服务")

    args = parser.parse_args(["--restart"])
    action = "启动" if args.start else ("停止" if args.stop else "重启" if args.restart else "未知")
    print(f"执行操作: {action}")


# ====================== 8. 参数分组 (argument groups) 美化帮助信息 ======================
def demo_groups():
    parser = argparse.ArgumentParser(description="参数分组（美化 help 输出）")

    input_group = parser.add_argument_group("输入参数")
    input_group.add_argument("--input", "-i", required=True, help="输入文件路径")
    input_group.add_argument("--format", choices=["json", "csv", "xml"], default="json", help="输入格式")

    output_group = parser.add_argument_group("输出参数")
    output_group.add_argument("--output", "-o", help="输出文件路径")
    output_group.add_argument("--overwrite", action="store_true", help="覆盖已有文件")

    args = parser.parse_args(["-i", "data.csv", "--format", "csv", "-o", "result.json"])
    print(f"输入: {args.input} ({args.format}), 输出: {args.output}, 覆盖: {args.overwrite}")


# ====================== 9. 子命令 / subparsers ======================
def demo_subparsers():
    parser = argparse.ArgumentParser(description="子命令示例（类似 git commit / git push）")
    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # add 子命令
    parser_add = subparsers.add_parser("add", help="添加任务")
    parser_add.add_argument("title", help="任务标题")
    parser_add.add_argument("--priority", type=int, choices=[1, 2, 3], default=2, help="优先级 1-3")

    # list 子命令
    parser_list = subparsers.add_parser("list", help="列出任务")
    parser_list.add_argument("--status", choices=["todo", "done", "all"], default="all", help="筛选状态")

    # delete 子命令
    parser_delete = subparsers.add_parser("delete", help="删除任务")
    parser_delete.add_argument("task_id", type=int, help="任务ID")

    # 模拟不同的命令行输入
    for cmd_args in [
        ["add", "学习Python", "--priority", "1"],
        ["list", "--status", "todo"],
        ["delete", "42"],
    ]:
        args = parser.parse_args(cmd_args)
        if args.command == "add":
            print(f"[add] 添加任务: '{args.title}', 优先级={args.priority}")
        elif args.command == "list":
            print(f"[list] 列出任务, 状态筛选: {args.status}")
        elif args.command == "delete":
            print(f"[delete] 删除任务 ID={args.task_id}")


# ====================== 10. 从文件读取参数 (fromfile_prefix_chars) ======================
def demo_fromfile():
    import tempfile
    parser = argparse.ArgumentParser(description="从文件读取参数", fromfile_prefix_chars="@")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--workers", type=int, default=4)
    # 使用 @ 前缀指定配置文件
    args = parser.parse_args(["--host", "0.0.0.0", "--workers", "8"])
    print(f"服务配置: {args.host}:{args.port}, workers={args.workers}")


# ====================== 11. 自定义 help / epilog / 格式化 ======================
def demo_help_format():
    parser = argparse.ArgumentParser(
        prog="myapp",
        description="自定义帮助信息格式化示例",
        epilog="更多信息请参考: https://docs.python.org/3/library/argparse.html",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--user", metavar="USERNAME", help="用户名")
    parser.add_argument("--passwd", metavar="PASSWORD", help="密码")
    args = parser.parse_args(["--user", "admin"])
    print(f"用户: {args.user}")


# ====================== 12. 自定义 Action 类 ======================
class RangeAction(argparse.Action):
    """自定义 Action：限制参数值在指定范围内"""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self.min = kwargs.pop("min", None)
        self.max = kwargs.pop("max", None)
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if self.min is not None and values < self.min:
            raise argparse.ArgumentError(self, f"{option_string} 不能小于 {self.min}，实际值: {values}")
        if self.max is not None and values > self.max:
            raise argparse.ArgumentError(self, f"{option_string} 不能大于 {self.max}，实际值: {values}")
        setattr(namespace, self.dest, values)


def demo_custom_action():
    parser = argparse.ArgumentParser(description="自定义 Action 示例")
    parser.add_argument("--percent", type=int, action=RangeAction, min=0, max=100,
                        help="百分比 (0-100)")
    args = parser.parse_args(["--percent", "85"])
    print(f"百分比: {args.percent}%")


# ====================== 13. 综合实战：文件处理工具 ======================
def demo_real_world():
    """模拟一个实用的命令行工具"""
    parser = argparse.ArgumentParser(
        prog="filetool",
        description="文件批量处理工具 - argparse 综合示例",
        epilog="示例: filetool convert -i data.csv -f json -o result.json"
    )

    subparsers = parser.add_subparsers(dest="cmd", help="操作命令")

    # convert 子命令
    p_convert = subparsers.add_parser("convert", help="文件格式转换")
    p_convert.add_argument("-i", "--input", required=True, help="输入文件")
    p_convert.add_argument("-f", "--format", choices=["json", "csv", "yaml"], default="json", help="目标格式")
    p_convert.add_argument("-o", "--output", help="输出文件（默认自动命名）")
    p_convert.add_argument("--pretty", action="store_true", help="美化输出")

    # info 子命令
    p_info = subparsers.add_parser("info", help="查看文件信息")
    p_info.add_argument("file", help="文件路径")
    p_info.add_argument("-v", "--verbose", action="count", default=0, help="详细级别")

    # batch 子命令
    p_batch = subparsers.add_parser("batch", help="批量处理")
    p_batch.add_argument("pattern", help="文件匹配模式，如 *.csv")
    p_batch.add_argument("-j", "--jobs", type=int, default=1, help="并行数 (默认 1)")
    p_batch.add_argument("--dry-run", action="store_true", help="预览模式，不实际执行")

    # 模拟不同命令
    test_cases = [
        ["convert", "-i", "data.csv", "-f", "json", "--pretty"],
        ["info", "document.txt", "-vv"],
        ["batch", "*.csv", "-j", "4", "--dry-run"],
    ]

    for cmd_args in test_cases:
        print(f"\n$ filetool {' '.join(cmd_args)}")
        args = parser.parse_args(cmd_args)
        if args.cmd == "convert":
            print(f"  转换: {args.input} -> {args.format}, pretty={args.pretty}")
        elif args.cmd == "info":
            print(f"  查看: {args.file}, verbose 级别={args.verbose}")
        elif args.cmd == "batch":
            print(f"  批量: {args.pattern}, jobs={args.jobs}, dry_run={args.dry_run}")


# ====================== 14. 真实用法：不传列表，自动读 sys.argv ======================
def demo_real_usage_hint():
    """
    前面的 demo 为了方便自测，传了硬编码列表给 parse_args([...])。
    但在真实脚本中你应该调用 parser.parse_args() —— 不加任何参数。
    它会自动读取 sys.argv，也就是终端里敲的命令。

    用法示例（在终端里执行）：
        python 11.argparse示例.py --name Tom -v
    """
    # 这里不实际执行，只是说明概念
    print("真实用法: parser.parse_args()  —— 不加参数，自动读命令行")


# ====================== 15. parse_known_args：忽略未知参数 ======================
def demo_parse_known_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--foo", default="bar")
    # 额外传入未知参数 --baz
    known, unknown = parser.parse_known_args(["--foo", "hello", "--baz", "123"])
    print(f"已知参数: foo={known.foo}")
    print(f"未知参数: {unknown}  (可传递给其他工具)")


# ====================== 入口 ======================
if __name__ == "__main__":
    print("========== 1. 基础用法 ==========")
    demo_basic()

    print("\n========== 2. 可选参数 ==========")
    demo_optional()

    print("\n========== 3. 类型转换 ==========")
    demo_type()

    print("\n========== 4. choices 限定值 ==========")
    demo_choices()

    print("\n========== 5. action 动作 ==========")
    demo_action()

    print("\n========== 6. nargs 参数数量 ==========")
    demo_nargs()

    print("\n========== 7. 互斥组 ==========")
    demo_mutually_exclusive()

    print("\n========== 8. 参数分组 ==========")
    demo_groups()

    print("\n========== 9. 子命令 ==========")
    demo_subparsers()

    print("\n========== 10. 从文件读取参数 ==========")
    demo_fromfile()

    print("\n========== 11. 自定义 help 格式 ==========")
    demo_help_format()

    print("\n========== 12. 自定义 Action ==========")
    demo_custom_action()

    print("\n========== 13. 综合实战 ==========")
    demo_real_world()

    print("\n========== 14. 真实用法 vs demo用法 ==========")
    demo_real_usage_hint()

    print("\n========== 15. parse_known_args ==========")
    demo_parse_known_args()
