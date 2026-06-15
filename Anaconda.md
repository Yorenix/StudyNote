# 基础操作

```
常用的conda指令：

创建新的python环境  conda create -n env_name python=3.x

查看已有的python环境  conda envlist

进入已有的python环境  conda activate env_name

退出当前的python环境  condadeactivate

常用的pip指令:

pip install -r requirements.txt  根据requirements.txt的内容安装所需的包

pip install package_name          安装包

pip install ............... --timeout6000

pip 换清华源后缀:

-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple--trusted-host=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

```

# 环境管理

```
创建环境（指定Python版本）	conda create -n <环境名> python=<版本>
激活环境	conda activate <环境名>
退出当前环境	conda deactivate
列出所有环境	conda env list 或 conda info --envs
删除环境	conda remove -n <环境名> --all
克隆环境	conda create -n <新环境名> --clone <被克隆环境名>
```

# 包管理

```
在当前环境安装包	conda install <包名>
在指定环境安装包	conda install -n <环境名> <包名>
安装指定版本的包	conda install <包名>=<版本号>
从特定频道安装	conda install -c <频道名> <包名>
更新单个包	conda update <包名>
更新当前环境所有包	conda update --all
卸载包	conda remove <包名>
查看已安装包	conda list
搜索可用包	conda search <包名>
```

# 环境导出与重建

```
导出完整环境配置（YAML）	conda env export > environment.yml
仅导出手动安装的包（推荐）	conda env export --from-history > environment.yml
通过YAML文件创建环境	conda env create -f environment.yml
```

# 配置优化（换源）

```
添加频道（如清华源）	pip install XXX -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple--trusted-host=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
设置频道优先级为严格	conda config --set channel_priority strict
查看当前配置的频道	conda config --show channels
恢复默认频道	conda config --remove-key channels
```

# 环境清理与维护

```
清理包缓存和索引	conda clean --all
查看环境修改历史	conda list -n <环境名> --revisions
回滚到指定修订版本	conda install -n <环境名> --revision <修订版本号>
查看Conda系统信息	conda info
更新Conda自身	conda update conda
更新Anaconda完整发行版	conda update anaconda
```

# 辅助与预览

```
预览安装/更新计划（不执行）	conda install <包名> --dry-run
自动确认所有提示	conda install <包名> --yes
查看全局帮助	conda --help
查看特定命令帮助	conda <命令> --help
```

# 常见问题解决



## 用虚拟环境启动jupyter notebook时候，jupyter notebook页面没有显示虚拟环境列表

```
python -m ipykernel install --user --name pytorchcpu --display-name "pytorchcpu"
```

![77601656174](C:\Users\21467\AppData\Local\Temp\1776016561746.png)

执行此操作后，重新启动jupyter notebook