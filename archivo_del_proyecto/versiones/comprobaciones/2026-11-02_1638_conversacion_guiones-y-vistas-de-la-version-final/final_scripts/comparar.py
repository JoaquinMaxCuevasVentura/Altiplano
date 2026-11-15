import subprocess, time, sys, uno
from com.sun.star.beans import PropertyValue
def prop(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p
new, old, out = sys.argv[1:4]
proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore", "--nologo",
                         "-env:UserInstallation=file:///tmp/lo_compare_profile",
                         "--accept=socket,host=localhost,port=2002;urp;"])
local = uno.getComponentContext()
resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
ctx = None
for _ in range(60):
    try:
        ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception:
        time.sleep(1)
smgr = ctx.ServiceManager
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(new), "_blank", 0, (prop("Hidden", True),))
disp = smgr.createInstanceWithContext("com.sun.star.frame.DispatchHelper", ctx)
frame = doc.getCurrentController().getFrame()
disp.executeDispatch(frame, ".uno:CompareDocuments", "", 0,
                     (prop("URL", uno.systemPathToFileUrl(old)), prop("NoAcceptDialog", True)))
n = doc.getRedlines().createEnumeration()
count = 0
while n.hasMoreElements():
    n.nextElement(); count += 1
print("cambios marcados:", count)
doc.storeToURL(uno.systemPathToFileUrl(out), (prop("FilterName", "MS Word 2007 XML"),))
doc.close(True)
try:
    desktop.terminate()
except Exception:
    pass
proc.wait(timeout=30)
