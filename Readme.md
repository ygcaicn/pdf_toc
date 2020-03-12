# pdf 目录挂载

# 命令行

```bash
$ ./toc.py --help
usage: toc.py [-h] sub-command  ...

positional arguments:
  sub-command 
    export      export toc of pdf
    mount       mount toc to pdf
    test        test toc file
    format      test toc file
    clean       clean toc

optional arguments:
  -h, --help    show this help message and exit

```

## demo

### 导出pdf文件目录

导出后可利用文本编辑器进行处理。

```bash
 # 直接输出
 ./toc.py export ~/Downloads/1.pdf
 
 # 保存到文件，默认使用1.pdf.txt作为toc文件
 ./toc.py export ~/Downloads/1.pdf -o

```

### 编辑toc文件

toc文件标准格式为：

'\t'*N+'name'+'@'+page

注意缩进全部采用Table，不能使用空格代替！

例如：

```bash
第 1 章 内核引导和初始化@1
	1.1 到哪里读取引导程序@1
	1.2 引导程序@1
		1.2.1 入口_start@1
		1.2.2 标号 reset@2
		1.2.3 函数_main@4
		1.2.4 函数 run_main_loop@6
	1.3 内核初始化@8
		1.3.1 汇编语言部分@8
		1.3.2 C 语言部分@11
		1.3.3 SMP 系统的引导@12
	1.4 init 进程@15
第 2 章 进程管理@17
	2.1 进程@17
	2.2 命名空间@18
	2.3 进程标识符@20
	2.4 进程关系@21
	2.5 启动程序@23
		2.5.1 创建新进程@23
		2.5.2 装载程序@41

```

可使用vsc进行正则替换处理toc文件。

常用替换正则：

1. 替换...->@

src:`\s*[\.]{2,}\s*`

dst:`@`


2. 二级目录缩进，例如：1.1

src:`(^\d+\.\d+[^.])`

src:`\t$1`

3. 三级目录缩进，例如：2.3.1

src:`(^\d+\.\d+\.\d+[^.])`

dst:`\t\t$1`


### 挂载目录到pdf文件

```bash
# 默认使用1.pdf.txt作为toc文件, 可使用-t选项指定
# -i指定基准页
# -c指定默认展开几级目录，默认1,0全部展开
./toc.py mount ~/Downloads/1.pdf -i 10 -c 2

```

# GUI

TODO: 待完成