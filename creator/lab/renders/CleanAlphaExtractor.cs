using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ThunderRender {
    public class CleanAlphaExtractor {
        public static void ExtractToPng(string inputPath, string outputPath) {
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

                    // Average background color from corners
                    int bgB = (srcBytes[0] + srcBytes[(w - 1) * 4] + srcBytes[(h - 1) * stride] + srcBytes[(h - 1) * stride + (w - 1) * 4]) / 4;
                    int bgG = (srcBytes[1] + srcBytes[(w - 1) * 4 + 1] + srcBytes[(h - 1) * stride + 1] + srcBytes[(h - 1) * stride + (w - 1) * 4 + 1]) / 4;
                    int bgR = (srcBytes[2] + srcBytes[(w - 1) * 4 + 2] + srcBytes[(h - 1) * stride + 2] + srcBytes[(h - 1) * stride + (w - 1) * 4 + 2]) / 4;

                    bool[,] isBg = new bool[w, h];
                    bool[,] visited = new bool[w, h];
                    Queue<Point> q = new Queue<Point>();

                    // Initialize queue with image boundary pixels
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

                    // Distance threshold for uniform dark studio backdrop (background varies by at most 3-4 units)
                    double maxDist = 12.0;

                    while (q.Count > 0) {
                        Point pt = q.Dequeue();
                        int x = pt.X;
                        int y = pt.Y;
                        int idx = y * stride + x * 4;

                        byte b = srcBytes[idx];
                        byte g = srcBytes[idx + 1];
                        byte r = srcBytes[idx + 2];

                        double dist = Math.Sqrt((r - bgR) * (r - bgR) + (g - bgG) * (g - bgG) + (b - bgB) * (b - bgB));

                        if (dist <= maxDist) {
                            isBg[x, y] = true;

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

                    // Build alpha channel with smooth edge anti-aliasing
                    byte[,] alpha = new byte[w, h];
                    for (int y = 0; y < h; y++) {
                        for (int x = 0; x < w; x++) {
                            if (isBg[x, y]) {
                                alpha[x, y] = 0;
                            } else {
                                alpha[x, y] = 255;
                            }
                        }
                    }

                    // Smooth edge feathering (1-pixel anti-aliasing)
                    for (int y = 1; y < h - 1; y++) {
                        for (int x = 1; x < w - 1; x++) {
                            if (!isBg[x, y]) {
                                int bgNeighbors = 0;
                                for (int i = 0; i < 8; i++) {
                                    if (isBg[x + dx[i], y + dy[i]]) bgNeighbors++;
                                }
                                if (bgNeighbors > 0) {
                                    int a = 255 - (bgNeighbors * 25);
                                    if (a < 50) a = 50;
                                    alpha[x, y] = (byte)a;
                                }
                            }
                        }
                    }

                    // Write destination bytes
                    for (int y = 0; y < h; y++) {
                        int row = y * stride;
                        for (int x = 0; x < w; x++) {
                            int idx = row + x * 4;
                            destBytes[idx + 3] = alpha[x, y];
                        }
                    }

                    Marshal.Copy(destBytes, 0, destData.Scan0, bytes);
                    src.UnlockBits(srcData);
                    dest.UnlockBits(destData);

                    dest.Save(outputPath, ImageFormat.Png);
                }
            }
        }
    }
}
