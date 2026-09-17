using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

internal sealed class Pet : Form
{
    [StructLayout(LayoutKind.Sequential)] struct POINT { public int x,y; public POINT(int a,int b){x=a;y=b;} }
    [StructLayout(LayoutKind.Sequential)] struct SIZE { public int cx,cy; public SIZE(int a,int b){cx=a;cy=b;} }
    [StructLayout(LayoutKind.Sequential, Pack=1)] struct BLEND { public byte op,flags,alpha,format; }
    [DllImport("user32.dll", SetLastError=true)] static extern bool UpdateLayeredWindow(IntPtr h,IntPtr dc,ref POINT dst,ref SIZE size,IntPtr src,ref POINT origin,int key,ref BLEND blend,int flags);
    [DllImport("user32.dll")] static extern IntPtr GetDC(IntPtr h);
    [DllImport("user32.dll")] static extern int ReleaseDC(IntPtr h,IntPtr dc);
    [DllImport("gdi32.dll")] static extern IntPtr CreateCompatibleDC(IntPtr dc);
    [DllImport("gdi32.dll")] static extern IntPtr SelectObject(IntPtr dc,IntPtr obj);
    [DllImport("gdi32.dll")] static extern bool DeleteObject(IntPtr obj);
    [DllImport("gdi32.dll")] static extern bool DeleteDC(IntPtr dc);
    [DllImport("user32.dll")] static extern bool SetProcessDPIAware();
    readonly Bitmap[][] frames = new Bitmap[11][];
    readonly int[][] times = {
        new[]{280,110,110,140,140,320}, new[]{120,120,120,120,120,120,120,220},
        new[]{120,120,120,120,120,120,120,220}, new[]{140,140,140,280},
        new[]{140,140,140,140,280}, new[]{140,140,140,140,140,140,140,240},
        new[]{150,150,150,150,150,260}, new[]{120,120,120,120,120,220},
        new[]{150,150,150,150,150,280}, new[]{150,150,150,150,150,150,150,150}, new[]{150,150,150,150,150,150,150,150}
    };
    readonly System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer();
    readonly NotifyIcon tray = new NotifyIcon();
    readonly ContextMenuStrip menu = new ContextMenuStrip();
    readonly string settings = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),"SilverBasketballPet","settings.txt");
    int row,frame,ticks,scale=100;
    bool dragging,paused,automatic=true;
    Point grab;
    readonly Random random = new Random();
    protected override bool ShowWithoutActivation { get { return true; } }
    protected override CreateParams CreateParams { get { var p=base.CreateParams; p.ExStyle |= 0x80000 | 0x80 | 0x08000000; return p; } }

    Pet()
    {
        Text="银发小篮球 · 独立桌宠";
        FormBorderStyle=FormBorderStyle.None; ShowInTaskbar=false; TopMost=true;
        StartPosition=FormStartPosition.Manual;
        using(var stream=Assembly.GetExecutingAssembly().GetManifestResourceStream("sprites.png"))
        using(var atlas=new Bitmap(stream)) {
            if(atlas.Width!=1536 || atlas.Height!=2288) throw new InvalidDataException("动画图集尺寸不正确");
            for(int r=0;r<11;r++) {
                frames[r]=new Bitmap[times[r].Length];
                for(int c=0;c<frames[r].Length;c++) frames[r][c]=atlas.Clone(new Rectangle(c*192,r*208,192,208),PixelFormat.Format32bppPArgb);
            }
        }
        Size=new Size(192,208);
        var area=Screen.PrimaryScreen.WorkingArea;
        Location=new Point(area.Right-Width-60,area.Bottom-Height-30);
        try {
            if(File.Exists(settings)) {
                var s=File.ReadAllLines(settings);
                scale=Math.Max(50,Math.Min(200,int.Parse(s[2])));
                Size=new Size(192*scale/100,208*scale/100);
                Location=new Point(int.Parse(s[0]),int.Parse(s[1]));
            }
        } catch { scale=100; Size=new Size(192,208); }
        Clamp();
        menu.Items.Add("银发小篮球 · 独立运行").Enabled=false;
        menu.Items.Add("自动互动",null,delegate { automatic=true; paused=false; Play(0); });
        var actions=new ToolStripMenuItem("播放动作");
        string[] names={"待机","向右跑","向左跑","挥手","跳跃","沮丧","等待","忙碌","观察"};
        for(int i=0;i<names.Length;i++) { int r=i; actions.DropDownItems.Add(names[i],null,delegate {automatic=false;paused=false;Play(r);}); }
        menu.Items.Add(actions);
        var pause=new ToolStripMenuItem("暂停动画");
        pause.CheckOnClick=true; pause.CheckedChanged+=delegate {paused=pause.Checked;}; menu.Items.Add(pause);
        var sizes=new ToolStripMenuItem("大小");
        foreach(int value in new[]{75,100,125,150,200}) { int v=value; sizes.DropDownItems.Add(v+"%",null,delegate {scale=v;Size=new Size(192*v/100,208*v/100);Clamp();Render();Save();}); }
        menu.Items.Add(sizes);
        menu.Items.Add("找回宠物（移到主屏）",null,delegate {var a=Screen.PrimaryScreen.WorkingArea;Location=new Point(a.Right-Width-60,a.Bottom-Height-30);Clamp();Render();});
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add("退出桌宠",null,delegate {Close();});
        ContextMenuStrip=menu;
        tray.Icon=SystemIcons.Application;tray.Text="银发小篮球（右键菜单，双击找回）";tray.ContextMenuStrip=menu;tray.Visible=true;
        tray.DoubleClick+=delegate {var a=Screen.PrimaryScreen.WorkingArea;Location=new Point(a.Right-Width-60,a.Bottom-Height-30);Clamp();Render();};
        MouseDown+=delegate(object sender,MouseEventArgs e){if(e.Button==MouseButtons.Left){dragging=true;grab=e.Location;Capture=true;}};
        MouseMove+=delegate {if(dragging){Location=new Point(Cursor.Position.X-grab.X,Cursor.Position.Y-grab.Y);Render();}};
        MouseUp+=delegate {if(dragging){dragging=false;Capture=false;Clamp();Render();Save();}};
        MouseDoubleClick+=delegate(object sender,MouseEventArgs e){if(e.Button==MouseButtons.Left){paused=false;Play(3);}};
        timer.Tick+=delegate {
            if(paused || dragging) return;
            frame++;
            if(frame>=frames[row].Length){frame=0;ticks++;if(automatic && row!=0){row=0;ticks=0;}else if(automatic && ticks>=5){row=random.Next(2)==0?3:4;ticks=0;}}
            Render();timer.Interval=times[row][frame];
        };
        Shown+=delegate {Play(0);timer.Start();};
        FormClosed+=delegate {Save();timer.Dispose();tray.Visible=false;tray.Dispose();menu.Dispose();foreach(var list in frames)foreach(var b in list)b.Dispose();};
    }
    void Play(int r){row=r;frame=0;ticks=0;timer.Interval=times[r][0];if(IsHandleCreated)Render();}
    void Clamp(){var a=Screen.FromRectangle(Bounds).WorkingArea;Location=new Point(Math.Max(a.Left,Math.Min(Left,a.Right-Width)),Math.Max(a.Top,Math.Min(Top,a.Bottom-Height)));}
    void Save(){try{Directory.CreateDirectory(Path.GetDirectoryName(settings));File.WriteAllLines(settings,new[]{Left.ToString(),Top.ToString(),scale.ToString()});}catch{/* Read-only profiles can still run the pet. */}}
    void Render()
    {
        using(var bitmap=new Bitmap(Width,Height,PixelFormat.Format32bppPArgb)) {
            using(var g=Graphics.FromImage(bitmap)) {g.CompositingMode=System.Drawing.Drawing2D.CompositingMode.SourceCopy;g.InterpolationMode=System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;g.DrawImage(frames[row][frame],new Rectangle(0,0,Width,Height));}
            IntPtr screen=GetDC(IntPtr.Zero),memory=IntPtr.Zero,hbitmap=IntPtr.Zero,old=IntPtr.Zero;
            try {
                memory=CreateCompatibleDC(screen);hbitmap=bitmap.GetHbitmap(Color.FromArgb(0));old=SelectObject(memory,hbitmap);
                var point=new POINT(Left,Top);var size=new SIZE(Width,Height);var source=new POINT(0,0);var blend=new BLEND{alpha=255,format=1};
                if(!UpdateLayeredWindow(Handle,screen,ref point,ref size,memory,ref source,0,ref blend,2))throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
            } finally {if(old!=IntPtr.Zero)SelectObject(memory,old);if(hbitmap!=IntPtr.Zero)DeleteObject(hbitmap);if(memory!=IntPtr.Zero)DeleteDC(memory);if(screen!=IntPtr.Zero)ReleaseDC(IntPtr.Zero,screen);}
        }
    }
    [STAThread] static void Main(string[] args)
    {
        SetProcessDPIAware();Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
        bool created;using(var mutex=new Mutex(true,"Local\\SilverBasketballDesktopPet",out created)) {
            if(!created)return;
            try {
                using(var pet=new Pet()) {
                    if(args.Length>0 && args[0]=="--smoke-test") {
                        int step=0;var check=new System.Windows.Forms.Timer{Interval=40};
                        check.Tick+=delegate {if(step<88){int r=step/8,c=step%8;pet.row=r;pet.frame=Math.Min(c,pet.frames[r].Length-1);pet.Render();step++;}else{check.Stop();check.Dispose();File.WriteAllText(Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"smoke-test.txt"),"PASS: 11 rows rendered through UpdateLayeredWindow; resources loaded; normal close.");pet.Close();}};
                        pet.Shown+=delegate {pet.timer.Stop();check.Start();};
                    }
                    Application.Run(pet);
                }
            }catch(Exception ex){File.WriteAllText(Path.Combine(Path.GetTempPath(),"SilverBasketballPet-error.txt"),ex.ToString());MessageBox.Show(ex.Message,"桌宠启动失败");Environment.ExitCode=1;}
        }
    }
}
