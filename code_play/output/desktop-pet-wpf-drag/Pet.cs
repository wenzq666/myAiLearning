using System;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;

[assembly: AssemblyTitle("Silver Basketball Desktop Pet")]
[assembly: AssemblyDescription("Local WPF animated desktop pet; source included")]
[assembly: AssemblyVersion("2.1.0.0")]

internal sealed class PetWindow : Window
{
    readonly Image picture = new Image();
    readonly BitmapSource[][] frames = new BitmapSource[9][];
    readonly DispatcherTimer timer = new DispatcherTimer();
    readonly int[][] durations = {
        new[]{280,110,110,140,140,320},new[]{120,120,120,120,120,120,120,220},
        new[]{120,120,120,120,120,120,120,220},new[]{140,140,140,280},
        new[]{140,140,140,140,280},new[]{140,140,140,140,140,140,140,240},
        new[]{150,150,150,150,150,260},new[]{120,120,120,120,120,220},
        new[]{150,150,150,150,150,280}
    };
    int row, frame;
    bool paused;
    bool dragging;
    Point dragAnchor;
    int previousRow, previousFrame;
    double horizontalTravel;

    public PetWindow()
    {
        Title = "银发小篮球 · WPF 桌宠";
        Width=192; Height=208;
        WindowStyle=WindowStyle.None; ResizeMode=ResizeMode.NoResize;
        AllowsTransparency=true; Background=Brushes.Transparent;
        Topmost=true; ShowInTaskbar=true; ShowActivated=false;
        var area=SystemParameters.WorkArea;
        Left=area.Right-Width-40; Top=area.Bottom-Height-30;
        var atlas=new BitmapImage();
        using(var stream=Assembly.GetExecutingAssembly().GetManifestResourceStream("sprites.png")) {
            atlas.BeginInit();atlas.CacheOption=BitmapCacheOption.OnLoad;
            atlas.StreamSource=stream;atlas.EndInit();atlas.Freeze();
        }
        if(atlas.PixelWidth!=1536 || atlas.PixelHeight!=2288)
            throw new InvalidOperationException("动画素材尺寸不正确。");
        for(int r=0;r<9;r++) {
            frames[r]=new BitmapSource[durations[r].Length];
            for(int c=0;c<frames[r].Length;c++) {
                var cell=new CroppedBitmap(atlas,new Int32Rect(c*192,r*208,192,208));
                cell.Freeze();frames[r][c]=cell;
            }
        }
        picture.Stretch=Stretch.Fill;Content=picture;
        var menu=new ContextMenu();
        var title=new MenuItem{Header="银发小篮球 · 本地动画",IsEnabled=false};menu.Items.Add(title);
        var actions=new MenuItem{Header="切换动作"};
        string[] names={"待机","向右跑","向左跑","挥手","跳跃","沮丧","等待","忙碌","观察"};
        for(int i=0;i<names.Length;i++) {
            int selected=i;var item=new MenuItem{Header=names[i]};
            item.Click+=delegate{Play(selected);};actions.Items.Add(item);
        }
        menu.Items.Add(actions);
        var pause=new MenuItem{Header="暂停动画",IsCheckable=true};
        pause.Click+=delegate{paused=pause.IsChecked;};menu.Items.Add(pause);
        var sizes=new MenuItem{Header="大小"};
        foreach(int percent in new[]{75,100,125,150,200}) {
            int value=percent;var item=new MenuItem{Header=value+"%"};
            item.Click+=delegate{Width=192*value/100.0;Height=208*value/100.0;Clamp();};sizes.Items.Add(item);
        }
        menu.Items.Add(sizes);
        var top=new MenuItem{Header="保持置顶",IsCheckable=true,IsChecked=true};
        top.Click+=delegate{Topmost=top.IsChecked;};menu.Items.Add(top);
        menu.Items.Add(new Separator());
        var quit=new MenuItem{Header="退出桌宠"};quit.Click+=delegate{Close();};menu.Items.Add(quit);
        ContextMenu=menu;
        MouseLeftButtonDown+=delegate(object sender,MouseButtonEventArgs e){
            if(e.ClickCount==2){EndDrag();Play(3);e.Handled=true;return;}
            if(e.ButtonState!=MouseButtonState.Pressed)return;
            dragAnchor=e.GetPosition(this);
            if(!CaptureMouse())return;
            previousRow=row;previousFrame=frame;horizontalTravel=0;dragging=true;
            Play(4); // Pick-up animation until horizontal movement selects a run.
            e.Handled=true;
        };
        MouseMove+=delegate(object sender,MouseEventArgs e){
            if(!dragging)return;
            if(e.LeftButton!=MouseButtonState.Pressed){EndDrag();return;}
            var position=e.GetPosition(this);
            double dx=position.X-dragAnchor.X,dy=position.Y-dragAnchor.Y;
            Left+=dx;Top+=dy;
            if(dx!=0){
                if(Math.Sign(dx)!=Math.Sign(horizontalTravel))horizontalTravel=0;
                horizontalTravel+=dx;
                if(Math.Abs(horizontalTravel)>=3){
                    int direction=horizontalTravel>0?1:2;
                    if(row!=direction)Play(direction);
                    horizontalTravel=0;
                }
            }
            e.Handled=true;
        };
        MouseLeftButtonUp+=delegate(object sender,MouseButtonEventArgs e){if(dragging){EndDrag();e.Handled=true;}};
        LostMouseCapture+=delegate{EndDrag();};
        Deactivated+=delegate{EndDrag();};
        KeyDown+=delegate(object sender,KeyEventArgs e){if(e.Key==Key.Escape)Close();};
        timer.Tick+=delegate{if((paused && !dragging) || menu.IsOpen)return;frame=(frame+1)%frames[row].Length;Draw();};
        Loaded+=delegate{Play(0);timer.Start();};
        Closed+=delegate{timer.Stop();};
    }
    void EndDrag(){
        if(!dragging)return;
        dragging=false;
        if(IsMouseCaptured)ReleaseMouseCapture();
        row=previousRow;frame=previousFrame;Draw();
    }
    void Play(int selected){row=selected;frame=0;Draw();}
    void Draw(){picture.Source=frames[row][frame];timer.Interval=TimeSpan.FromMilliseconds(durations[row][frame]);}
    void Clamp(){var a=SystemParameters.WorkArea;Left=Math.Max(a.Left,Math.Min(Left,a.Right-Width));Top=Math.Max(a.Top,Math.Min(Top,a.Bottom-Height));}
    [STAThread] public static void Main()
    {
        try {new Application().Run(new PetWindow());}
        catch(Exception error){MessageBox.Show("桌宠无法启动："+error.Message,"银发小篮球");}
    }
}
