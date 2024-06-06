from DrissionPage import ChromiumOptions,ChromiumPage
path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
co = ChromiumOptions()
co.set_browser_path(path).save()
co.ignore_certificate_errors(True)

cp = ChromiumPage()

cp.get("https://202.202.32.120:8443/Self/login/")

cp.ele("css:#account").input("")
cp.ele("css:#password").input("")
cp.ele("css:.btn.btn-primary.btn-block").click()

response = cp.listen.wait().response

