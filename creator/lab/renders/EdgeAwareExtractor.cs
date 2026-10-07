using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ThunderRender {
    public class EdgeAwareExtractor {
        public static void Extract(string inputPath, string outputPath) {
            using (Bitmap src = new Bitmap(inputPath)) {
                int w = src.Width;
                int h = src.Height;

                using (Bitmap dest = new Bitmap(w, h, PixelFormat.Format32bppArgb)) {
                    BitmapData srcData = src.LockBits(new Rectangle(0, 0, w, h), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
                    BitmapData destData = dest.LockBits(new Rectangle(0, 0, w, h), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);

                    int stride = srcData.Stride;
                    int bytes = stride * h;
                    byte[] srcBytes = new byte[bytes];
                    byte[] destBytes = new byte[bytes];

                    Marshal.Copy(srcData.Scan0, srcBytes, 0, bytes);
                    Array.Copy(srcBytes, destBytes, bytes);

                    // Compute gradient magnitude (Sobel / simple gradient)
                    byte[,] edge = new byte[w, h];
                    for (int y = 1; y < h - 1; y++) {
                        int rPrev = (y - 1) * stride;
                        int rCurr = y * stride;
                        int rNext = (y + 1) * stride;
                        for (int x = 1; x < w - 1; x++) {
                            int lumCenter = (srcBytes[rCurr + x * 4] + srcBytes[rCurr + x * 4 + 1] + srcBytes[rCurr + x * 4 + 2]) / 3;
                            int lumRight  = (srcBytes[rCurr + (x + 1) * 4] + srcBytes[rCurr + (x + 1) * 4 + 1] + srcBytes[rCurr + (x + 1) * 4 + 2]) / 3;
                            int lumDown   = (srcBytes[rNext + x * 4] + srcBytes[rNext + x * 4 + 1] + srcBytes[rNext + x * 4 + 2]) / 3;
                            int gx = Math.Abs(lumRight - lumCenter);
                            int gy = Math.Abs(lumDown - lumCenter);
                            int grad = gx + gy;
                            edge[x, y] = (byte)(grad > 255 ? 255 : grad);
                        }
                    }

                    int bgB = srcBytes[0];
                    int bgG = srcBytes[1];
                    int bgR = srcBytes[2];

                    bool[,] isBg = new bool[w, h];
                    bool[,] visited = new bool[w, h];
                    Queue<Point> q = new Queue<Point>();

                    // Enqueue outer border pixels
                    for (int x = 0; x < w; x++) {
                        q.Enqueue(new Point(x, 0));
                        q.Enqueue(new Point(x, h - 1));
                        visited[x, 0] = true;
                        visited[x, h - 1] = true;
                    }
                    for (int y = 0; y < h; y++) {
                        q.Enqueue(new Point(0, y));
                        q.Enqueue(new Point(w - 1, y));
                        visited[0, y] = true;
                        visited[w - 1, y] = true;
                    }

                    int[] dx = { 0, 0, 1, -1, 1, -1, 1, -1 };
                    int[] dy = { 1, -1, 0, 0, 1, 1, -1, -1 };

                    while (q.Count > 0) {
                        Point pt = q.Dequeue();
                        int x = pt.X;
                        int y = pt.Y;
                        int idx = y * stride + x * 4;

                        byte b = srcBytes[idx];
                        byte g = srcBytes[idx + 1];
                        byte r = srcBytes[idx + 2];

                        double dist = Math.Sqrt(Math.Pow(r - bgR, 2) + Math.Pow(g - bgG, 2) + Math.Pow(b - bgB, 2));

                        // Stop at strong edges or when color differs significantly from studio background
                        if (dist <= 75.0 && edge[x, y] < 22) {
                            isBg[x, y] = true;
                            destBytes[idx + 3] = 0;

                            for (int i = 0; i < 8; i++) {
                                int nx = x + dx[i];
                                int ny = y + dy[i];
                                if (nx >= 0 && nx < w && ny >= 0 && ny < h && !visited[nx, ny]) {
                                    visited[nx, ny] = true;
                                    q.Enqueue(new Point(nx, ny));
                                }
                            }
                        }
                    }

                    src.UnlockBits(srcData);
                    Marshal.Copy(destBytes, 0, destData.Scan0, bytes);
                    dest.UnlockBits(destData);

                    dest.Save(outputPath, ImageFormat.Png);
                }
            }
        }
    }
}
