using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ThunderRender {
    public class AvatarPngExtractor {
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

                    // Reference background color sampled from corners
                    int bgB = srcBytes[0];
                    int bgG = srcBytes[1];
                    int bgR = srcBytes[2];

                    bool[,] isBg = new bool[w, h];
                    bool[,] visited = new bool[w, h];
                    Queue<Point> q = new Queue<Point>();

                    // Initialize flood-fill from all image outer borders
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

                    // Color tolerance for flat studio background:
                    // Euclidean distance in RGB color space
                    double threshold = 55.0;

                    while (q.Count > 0) {
                        Point pt = q.Dequeue();
                        int x = pt.X;
                        int y = pt.Y;
                        int idx = y * stride + x * 4;

                        byte b = srcBytes[idx];
                        byte g = srcBytes[idx + 1];
                        byte r = srcBytes[idx + 2];

                        double dist = Math.Sqrt(Math.Pow(r - bgR, 2) + Math.Pow(g - bgG, 2) + Math.Pow(b - bgB, 2));

                        if (dist <= threshold) {
                            isBg[x, y] = true;
                            destBytes[idx + 3] = 0; // Fully transparent

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

                    // Smooth edge feathering for perfect anti-aliasing
                    for (int y = 1; y < h - 1; y++) {
                        for (int x = 1; x < w - 1; x++) {
                            if (!isBg[x, y]) {
                                int bgCount = 0;
                                for (int i = 0; i < 4; i++) {
                                    if (isBg[x + dx[i], y + dy[i]]) bgCount++;
                                }
                                if (bgCount > 0) {
                                    int idx = y * stride + x * 4;
                                    byte b = srcBytes[idx];
                                    byte g = srcBytes[idx + 1];
                                    byte r = srcBytes[idx + 2];
                                    double dist = Math.Sqrt(Math.Pow(r - bgR, 2) + Math.Pow(g - bgG, 2) + Math.Pow(b - bgB, 2));
                                    if (dist < threshold + 15.0) {
                                        double alpha = (dist - threshold) / 15.0;
                                        if (alpha < 0.2) alpha = 0.2;
                                        if (alpha > 1.0) alpha = 1.0;
                                        destBytes[idx + 3] = (byte)(alpha * 255);
                                    }
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
