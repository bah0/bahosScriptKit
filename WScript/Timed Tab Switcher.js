// small wscript code to switch between tabs in Firefox using keyboard emulation

var oShell = WScript.CreateObject("WScript.Shell");
oShell.AppActivate("Firefox"); // Set focus to a program
var x = 0;

while(x < 2){
oShell.SendKeys("^2");       // Ctrl+2
WScript.Sleep(60000);

oShell.SendKeys("^1");       // Ctrl+1
WScript.Sleep(60000);
//x = x+1;
}

WScript.Echo( "done!" );