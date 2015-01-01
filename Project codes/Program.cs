using System;
using System.Windows.Forms;
using InputManager;
using System.IO;

namespace NFSKeys
{
    class Program
    {
        static char fwd, L, R;
        static int state = 0;
        static int count = 0;
        static int pwm = 0;
        static Boolean cycle_done = false;
        static Boolean press_phase_done = false;
        static Boolean release_phase_done = false;

        static void Main(string[] args)
        {
            Console.WriteLine("Starting program");

            MicroTimer mt = new MicroTimer();
            mt.MicroTimerElapsed += new MicroTimer.MicroTimerElapsedEventHandler(ButtonPress);
            mt.Interval = 100;
            mt.Enabled = true;
            
            while (true)
            {
                try
                {
                    FileStream fs = new FileStream("C:/Temp/control.txt", FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
                    StreamReader sr = new StreamReader(fs);
                    String line1 = sr.ReadLine();
                    String line2 = sr.ReadLine();
                    sr.Close();
                                        
                    fwd = line1[0];
                    R = line1[1];
                    L = line1[2];
                    pwm = Convert.ToInt32(line2);

                    if (fwd == '1' && state == 0)
                    {
                        Keyboard.KeyDown(Keys.Up);
                        state = 1;
                    }

                    else if (fwd == '0' && state == 1)
                    {
                        Keyboard.KeyUp(Keys.Up); 
                        state = 0;
                    }

                    while (true)
                    {
                        if (cycle_done)
                            break;
                    }
                    cycle_done = false;
                    press_phase_done = false;
                    release_phase_done = false;
                    count = 0;
                }

                catch (Exception e)
                {
                    continue;
                }
            }
        }

        private static void ButtonPress(object sender, MicroTimerEventArgs timerEventArgs)
        {
            count++;

            if (count <= pwm && !press_phase_done && fwd == '1')
            {
                press_phase_done = true;
                if (L == '0' && R == '1')
                    Keyboard.KeyDown(Keys.Right);
                else if (L == '1' && R == '0')
                    Keyboard.KeyDown(Keys.Left);
            }

            else if (count > pwm && !release_phase_done)
            {
                release_phase_done = true;
                if (L == '0' && R == '1')
                    Keyboard.KeyUp(Keys.Right);
                else if (L == '1' && R == '0')
                    Keyboard.KeyUp(Keys.Left);
            }

            else if (count > 100)
                cycle_done = true;   
        }
    }
}
