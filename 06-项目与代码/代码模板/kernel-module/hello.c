// 最小内核模块（W12 D6：在板上加载自建 .ko）
// 板上执行：insmod hello.ko ; dmesg | tail ; rmmod hello
// 加载失败先查：uname -r 与 modinfo hello.ko 里的 vermagic 是否一致
#include <linux/init.h>
#include <linux/module.h>

static int __init hello_init(void)
{
	pr_info("hello: loaded\n");
	return 0;
}

static void __exit hello_exit(void)
{
	pr_info("hello: unloaded\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("minimal hello module for W12");
