---
title: 一些 Zsh 的配置记录
date: 2022-04-18 01:04:00
tags:
    - Linux
---

## 前言

今天用了一下 [`tmoe`](https://github.com/2moe/tmoe-linux)
发现有一些配置有点爽有点好看，就记录一下

### zsh 配置

#### 主题

- powerlevel10k
- agnoster
- agnosterzak

#### zsh 增强

- [Oh My Zsh](https://github.com/romkatv/powerlevel10k#oh-my-zsh)
- [zinit 插件管理器](https://github.com/zdharma-continuum/zinit)

#### zsh 插件

- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) —— 自动补全
- [fast-syntax-highlighting](https://github.com/zdharma-continuum/fast-syntax-highlighting) —— 命令高亮
- [colored-man-pages](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/colored-man-pages) —— 彩色 man
- [command-not-found](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/command-not-found) —— 显示未找到的命令来源于哪个软件包
- [extra](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/extract) —— 一键解压压缩包
- [sudo](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/sudo) —— 按两下 esc 将命令转换为 sudo
- [fzf-tab](https://github.com/Aloxaf/fzf-tab) —— aloxaf:fzf-tab 能够极大提升 zsh 补全体验，它通过 hook zsh 补全系统的底层函数 compadd 来截获补全列表，从而实现了在补全命令行参数、变量、目录栈和文件时都能使用 fzf 进行选择

### 一些有用的程序

- micro —— 文本编辑器
- exa —— 更好的 ls
- [bat](https://github.com/sharkdp/bat) —— 更好的 cat

### 一些有用的 alicas

```sh
alias grep='grep --color=auto'

if [[ $(command -v exa) ]] {
    DISABLE_LS_COLORS=true
    unset LS_BIN_FILE
    for i (/bin/ls /usr/bin/ls /usr/local/bin/ls) {
        [[ ! -x ${i} ]] || {
            local LS_BIN_FILE=${i}
            break
        }
    }
    [[ -n ${LS_BIN_FILE} ]] || local LS_BIN_FILE=$(whereis ls 2>/dev/null | awk '{print $2}')
    alias lls="${LS_BIN_FILE} -F --color=auto"
    # lls is the original ls. lls为原版ls
    alias ls="exa --color=auto"
    # Exa is a modern version of ls. exa是一款优秀的ls替代品,拥有更好的文件展示体验,输出结果更快,使用rust编写。
    alias l='exa -lbah --icons --color=auto'
    alias la='exa -lbagh --icons --color=auto'
    alias ll='exa -lbg --icons --color=auto'
    alias lsa='exa -lbagR --icons --color=auto'
    alias lst='exa -lTabgh --icons --color=auto' # 输入lst,将展示类似于tree的树状列表。
} else {
    alias ls='ls -F --color=auto'
    alias l='ls -lahF --color=auto'
    alias la='ls -lAhF --color=auto'
    alias ll='ls -lhF --color=auto'
    alias lsa='ls -lahF --color=auto'
    alias lst='tree -pCsh --color=auto'
}

set_bat_paper_variable() {
    unset CAT_BIN_FILE i
    for i (/bin/cat /usr/bin/cat /usr/local/bin/cat) {
        [[ ! -x ${i} ]] || {
            local CAT_BIN_FILE=${i}
            unset i
            break
        }
    }
    [[ -n ${CAT_BIN_FILE} ]] || local CAT_BIN_FILE=$(whereis cat 2>/dev/null | awk '{print $2}')
    alias lcat=${CAT_BIN_FILE}
    # lcat is the original cat.
    typeset -g BAT_PAGER="less -m -RFQ" # You can type q to quit bat. 输q退出bat的页面视图
}
# bat supports syntax highlighting for a large number of programming and markup languages. bat是cat的替代品，支持多语言语法高亮。
for i (batcat bat) {
    if [[ $(command -v ${i}) ]] {
        alias cat="${i} -pp"
        set_bat_paper_variable
        break
    }
}
```
