 os.environ.get('BILI_USER') and os.environ.get('BILI_PASS'):
        # 原有单账号逻辑，暂不支持多账号
        b = Bilibili()
        login = b.login(username=os.environ['BILI_USER'], password=os.environ['BILI_PASS'])
        if not login:
            sendNotify.send(title=u"哔哩哔哩签到", msg="登录失败 账号或密码错误，详情前往Github查看")
            exit(0)
        _bilibili_cookie_list = b.get_cookies()
        BiliBiliCheckIn(bilibili_cookie_list=_bilibili_cookie_list).main()
    elif os.environ.get('BILI_COOKIE'):
        BILI_COOKIE = os.environ['BILI_COOKIE']
        # 分割多个Cookie，每个账号的Cookie用&&分隔
        cookies_list = BILI_COOKIE.split('&&')
        for i, cookie_str in enumerate(cookies_list, 1):
            if i == 2:
                break
            cookie_str = cookie_str.strip()
            # sendNotify.send(title=u"哔哩cookie", msg=cookie_str)
            if not cookie_str:
                continue
            # 解析单个账号的Cookie
            cookie_dict = {}
            for c in cookie_str.split(';'):
                c = c.strip()
                if '=' in c:
                    key, val = c.split('=', 1)
                    cookie_dict[key.strip()] = val.strip()
            # 执行签到
            print(f"正在处理第 {i} 个账号")
            BiliBiliCheckIn(bilibili_cookie_list=cookie_dict).main()
    else:
        print("未提供有效的哔哩哔哩账号信息或Cookie，运行取消")
        exit(0)
