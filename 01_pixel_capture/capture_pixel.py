'''
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

// Drawing und Forms muss als Verweis hinzugenommen werden unter Projekteigenschaften
using System.Drawing;
using System.Windows.Forms;

//UdpClient
using System.Net.Sockets;

//Win32Exception
using System.ComponentModel;

namespace ConsoleApplication2
{
    class Program
    {
        static void Main(string[] args)
        {
            //string dst_ip = "10.176.18.162";
            //string dst_ip = "10.176.18.100";
            string version = "0.2";
            string dst_ip;
            int ms_sleep = 13;
            if (args.Length == 1 | args.Length == 2)
            {
                dst_ip = args[0];

                if (args.Length == 2)
                {
                    ms_sleep = Int32.Parse(args[1]);
                }
            } 
            else
            {
                System.Console.WriteLine("Please specify receiver IP for UDP packets.");
                System.Console.WriteLine("Usage: ConsoleApplication2 <ip, e.g. 192.168.1.2>");
                //System.Console.WriteLine("Starting with default IP");
                return;
            }

            System.Console.WriteLine("starting Pixel-ZZZ ...");
            System.Console.WriteLine("version is: "+version);
            System.Console.WriteLine("destination ip is: "+dst_ip);
            System.Console.WriteLine("thread sleep in msecs is: "+ms_sleep);

            int src_port = 8889;
            int dst_port = 8887;

            Bitmap map = new Bitmap(1, 1);
            Graphics graphics = Graphics.FromImage(map);
            Point p = new Point(0, 0);
            Size s = new Size(1, 1);
            Color color;

            UdpClient uc = new UdpClient(src_port); //src port
            byte[] msg;
            string msg_str;
            //msg = Encoding.ASCII.GetBytes("Hello!\n");
            //uc.Send(msg, msg.Length, dst_ip, dst_port);
            Int32 tc = Environment.TickCount;
            Int32 old_tc = tc;

            int evc = 0;
            int val;
            int old_val = 0;

            while (true) {
                try
                {
                    graphics.CopyFromScreen(p, p, s);
                }
                catch (Win32Exception w)
                {
                    Console.WriteLine("Warning: Win32Exception occurred. Sleeping 10 secs.");
                    System.Threading.Thread.Sleep(TimeSpan.FromMilliseconds(10000));
                }
                
                color = map.GetPixel(0, 0);
                val = color.R + color.G + color.B;
                if (val != old_val) {
                    tc = Environment.TickCount;
                    Console.WriteLine("E_{0:D3}: {1} [{2}]", evc, val, tc);
                    Console.WriteLine("I_{0:D3}: {1}\\{2},{3} [{4}]", evc ,old_val, val, (tc - old_tc), tc);
                    //msg = Encoding.ASCII.GetBytes("I_{0:D3}: " + old_val + "\\" + val + "," + (tc - old_tc) + " [" + tc + "]" + "\n");
                    msg_str = String.Format("I_{0:D3}: {1}\\{2},{3} [{4}]\n", evc, old_val, val, (tc - old_tc), tc);
                    msg = Encoding.ASCII.GetBytes(msg_str);
                    uc.Send(msg, msg.Length, dst_ip, dst_port);
                    Console.WriteLine("udp");
                    Console.WriteLine(msg.Length);
                    evc++;
                    if (evc == 1000)
                    {
                        evc = 0;
                    }
                    old_tc = tc;
                    old_val = val;
                }
                // 75 Hz
                System.Threading.Thread.Sleep(TimeSpan.FromMilliseconds(ms_sleep));
            }
        }
    
        static void SendUdp(int srcPort, string dstIp, int dstPort, byte[] data)
        {
            using (UdpClient c = new UdpClient(srcPort))
            c.Send(data, data.Length, dstIp, dstPort);
        }

    }

}
'''
print("hello world")

'''
def get_pixel_colour(i_x, i_y):
	import PIL.Image # python-imaging
	import PIL.ImageStat # python-imaging
	import Xlib.display # python-xlib
	o_x_root = Xlib.display.Display().screen().root
	o_x_image = o_x_root.get_image(i_x, i_y, 1, 1, Xlib.X.ZPixmap, 0xffffffff)
	o_pil_image_rgb = PIL.Image.fromstring("RGB", (1, 1), o_x_image.data, "raw", "BGRX")
	lf_colour = PIL.ImageStat.Stat(o_pil_image_rgb).mean
	return tuple(map(int, lf_colour))
 
print(get_pixel_colour(0, 0))
'''
