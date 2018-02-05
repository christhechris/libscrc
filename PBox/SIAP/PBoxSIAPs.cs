using System;
using System.Collections.Generic;
using System.Text;

using System.IO;
using System.Net;
using System.Threading;
using System.Net.Sockets;
using System.Collections;
using System.Web.Script.Serialization;

namespace PBoxSIAPs
{
    public class HttpProcessor
    {
        public TcpClient socket;
        public HttpServer srv;

        private StreamReader inputStream;
        public StreamWriter outputStream;

        public String http_method;
        public String http_url;
        public String http_protocol_versionstring;
        public Hashtable httpHeaders = new Hashtable();


        private static int MAX_POST_SIZE = 10 * 1024 * 1024; // 10MB

        public HttpProcessor(TcpClient s, HttpServer srv)
        {
            this.socket = s;
            this.srv = srv;
        }

        public void process()
        {
            inputStream = new StreamReader(socket.GetStream());
            outputStream = new StreamWriter(new BufferedStream(socket.GetStream()));
            try
            {
                parseRequest();
                readHeaders();
                if (http_method.Equals("GET"))
                {
                    handleGETRequest();
                }
                else if (http_method.Equals("POST"))
                {
                    handlePOSTRequest();
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: " + e.ToString());
                writeFailure();
            }
            try
            {
                outputStream.Flush();
            }
            catch (Exception e)
            {
                Console.WriteLine("**********Exception: " + e.ToString());
            }
            inputStream = null; outputStream = null; // bs = null;            
            socket.Close();
        }

        public void parseRequest()
        {
            String request = "";
            try
            {
                request = inputStream.ReadLine();
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: " + e.ToString());
            }

            string[] tokens = request.Split(' ');
            if (tokens.Length != 3)
            {
                throw new Exception("invalid http request line");
            }
            http_method = tokens[0].ToUpper();
            http_url = tokens[1];
            http_protocol_versionstring = tokens[2];

            Console.WriteLine("starting: " + request);
        }

        public void readHeaders()
        {
            Console.WriteLine("readHeaders()");
            String line;
            while ((line = inputStream.ReadLine()) != null)
            {
                if (line.Equals(""))
                {
                    Console.WriteLine("got headers");
                    return;
                }

                int separator = line.IndexOf(':');
                if (separator == -1)
                {
                    throw new Exception("invalid http header line: " + line);
                }
                String name = line.Substring(0, separator);
                int pos = separator + 1;
                while ((pos < line.Length) && (line[pos] == ' '))
                {
                    pos++; // strip any spaces
                }

                string value = line.Substring(pos, line.Length - pos);
                Console.WriteLine("header: {0}:{1}", name, value);
                httpHeaders[name] = value;
            }
        }

        public void handleGETRequest()
        {
            srv.handleGETRequest(this);
        }

        public void handlePOSTRequest()
        {
            Console.WriteLine("Get post data start");
            int content_len = 0;
            MemoryStream ms = new MemoryStream();

            if (this.httpHeaders.ContainsKey("Content-Length"))
            {
                content_len = Convert.ToInt32(this.httpHeaders["Content-Length"]);
                if ((content_len > MAX_POST_SIZE) || (content_len == 0))
                {
                    throw new Exception(
                        String.Format("POST Content-Length({0}) too big (or zero) for this simple server",
                          content_len));
                }

                char[] buf = new char[4096];
                int to_read = content_len;
                while (to_read > 0)
                {
                    try
                    {
                        int numread = this.inputStream.Read(buf, 0, to_read);
                        if (numread == 0)
                        {
                            ms.Write(Encoding.UTF8.GetBytes("<ERROR>"), 0, numread);
                            break;
                        }
                        to_read -= numread;
                        ms.Write(Encoding.UTF8.GetBytes(buf), 0, numread);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("**********Exception: " + e.ToString());
                    }
                }
                ms.Seek(0, SeekOrigin.Begin);

            }
            Console.WriteLine("Get post data end");
            srv.handlePOSTRequest(this, new StreamReader(ms));

        }

        public void writeSuccess()
        {
            outputStream.Write("HTTP/1.0 200 OK\n");
            outputStream.Write("Content-Type: text/html\n");
            outputStream.Write("Connection: close\n");
            outputStream.Write("\n");
        }

        public void writeFailure()
        {
            outputStream.Write("HTTP/1.0 404 File not found\n");
            outputStream.Write("Connection: close\n");
            outputStream.Write("\n");
        }
    }

    public abstract class HttpServer
    {
        protected string ip;
        protected int port;
        TcpListener listener;
        bool is_active = true;

        public HttpServer(string ip, int port)
        {
            this.ip = ip;
            this.port = port;
        }

        public void listen()
        {
            listener = new TcpListener(IPAddress.Parse(ip), port);
            listener.Start();
            while (is_active)
            {
                TcpClient s = listener.AcceptTcpClient();
                HttpProcessor processor = new HttpProcessor(s, this);
                Thread thread = new Thread(new ThreadStart(processor.process));
                thread.Start();
                Thread.Sleep(1);
            }
        }

        public abstract void handleGETRequest(HttpProcessor p);
        public abstract void handlePOSTRequest(HttpProcessor p, StreamReader inputData);
    }

    #region PBoxSIAP

    public class PBoxSIAPTypes
    {
        public class PBoxItemType
        {
            public string itemName;
            public string itemType;
        }

        public List<PBoxItemType> items;

        public string Get(int size)
        {
            List<PBoxItemType> tList = new List<PBoxItemType>();
            PBoxSIAPTypes siapTypes = new PBoxSIAPTypes();

            for (int i = 0; i < size; i++)
            {
                PBoxItemType item = new PBoxItemType
                {
                    itemName = "CSharp" + i.ToString(),
                    itemType = "INT32"
                };
                tList.Add(item);
            }
            siapTypes.items = tList;

            JavaScriptSerializer serialzer = new JavaScriptSerializer();
            return serialzer.Serialize(siapTypes);
        }
    }


    public class PBoxSIAPValues
    {
        public class PBoxDataValue
        {
            public string itemName;
            public int value;
        }

        public List<PBoxDataValue> items;

        public string Get(int size)
        {
            List<PBoxDataValue> eList = new List<PBoxDataValue>();
            PBoxSIAPValues siapValues = new PBoxSIAPValues();

            for (int i = 0; i < size; i++)
            {
                PBoxDataValue val = new PBoxDataValue
                {
                    itemName = "CSharp" + i.ToString(),
                    value = i
                };
                eList.Add(val);
            }
            siapValues.items = eList;

            JavaScriptSerializer serialzer = new JavaScriptSerializer();
            return serialzer.Serialize(siapValues);
        }
    }
    #endregion

    public class MyHttpServer : HttpServer
    {
        public MyHttpServer(string ip, int port)
            : base(ip, port)
        {
        }

        public override void handleGETRequest(HttpProcessor p)
        {
            int BlockSize = 20;
            String StrReq = "";
            Console.WriteLine("Get request: {0}", p.http_url);

            if (p.http_url.Contains("dataitems"))
            {
                PBoxSIAPTypes SiapTypes = new PBoxSIAPTypes();
                StrReq = SiapTypes.Get(BlockSize);
            }

            if (p.http_url.Contains("get"))
            {
                PBoxSIAPValues SiapValues = new PBoxSIAPValues();
                StrReq = SiapValues.Get(BlockSize);
            }

            try
            {
                p.writeSuccess();
                p.outputStream.WriteLine(StrReq);
            }
            catch (Exception e)
            {
                Console.WriteLine("**********Exception: " + e.ToString());
            }

            Console.WriteLine(StrReq);
        }

        public override void handlePOSTRequest(HttpProcessor p, StreamReader inputData)
        {
            string data = inputData.ReadToEnd();
            try
            {
                p.writeSuccess();
                p.outputStream.WriteLine(data);
            }
            catch (Exception e)
            {
                Console.WriteLine("**********Exception: " + e.ToString());
            }
            Console.WriteLine("POST request: {0}", p.http_url);
            Console.WriteLine("POST Message: {0}", data);
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            HttpServer httpServer;
            string SiapServerIP = "192.168.0.33";
            int SiapServerPort = 888;

            httpServer = new MyHttpServer(SiapServerIP, SiapServerPort);
            Console.WriteLine("Start Server: {0}:{1}", SiapServerIP, SiapServerPort);
            Thread thread = new Thread(new ThreadStart(httpServer.listen));
            thread.Start();
        }
    }
}
