'''
写在前面：为了方便大家能够开发的更加轻松顺利，
我大致的安排了一下程序的框架，
(实际上为了总结出来一个方便的框架我花了很多很多很多时间，
还希望大家赏脸仔细阅读)
大家查看自己负责部分内容，将代码写在对应位置即可
有需要改动的地方请大家指出或者直接修改

1.程序结构框架:
package app
    main.init：项目初始化，模块初始化（包括蓝本注册登录注册等等全部模块）
    main.errors：存储错误处理程序
    main.forms：处理表单信息（登录注册等）
    main.routes：路由模块，集中存储路由和内部方法函数。
                （就是书上的views）
    static
    templates：模板package，包含所需所有页面模板的前端设计
                页面设计后会被routes调用，在对应路由展示对应页面。
    app.init:
    app.email:
    app.models:数据库的模型衍射，核心内容。
    migrations：数据库迁移脚本
package tests：单元测试package，大家自行新建测试文件，随便搞。
                建议每个人命名格式为
                NameFunctionNameTest
venv虚拟环境
config：配置文件，初步写了一些，后期再加。
        包含环境数据库密钥等等。
        初始化时会被调用并配置。
manage：程序主入口，执行主入口运行整个项目
requirements：列出依赖包，便于在电脑生成虚拟环境
'''