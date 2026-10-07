using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ThunderRender {
    public class BackgroundRemover {
        public static void CreateTransparentPng(string inputPath, string outputPath) {
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

                    bool[,] isBg = new bool[w, h];
                    bool[,] visited = new bool[w, h];
                    Queue<Point> q = new Queue<Point>();

                    // Start from outer image edges
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

                    // Background in valyr_avatar_discord_1 is neutral charcoal grey:
                    // R is ~18..32, G is ~20..35, B is ~22..38.
                    // Highly neutral (saturation < 12%)
                    while (q.Count > 0) {
                        Point pt = q.Dequeue();
                        int x = pt.X;
                        int y = pt.Y;
                        int idx = y * stride + x * 4;

                        byte b = srcBytes[idx];
                        byte g = srcBytes[idx + 1];
                        byte r = srcBytes[idx + 2];

                        int maxC = Math.Max(r, Math.Max(g, b));
                        int minC = Math.Min(r, Math.Min(g, b));
                        int chroma = maxC - minC;

                        // Condition for studio dark background:
                        // 1. Low brightness (max channel <= 45)
                        // 2. Low saturation / neutral tint (chroma <= 10)
                        // 3. Not deeply blue or warm (book is warm R>B+20, cape is blue B>R+10)
                        bool isBackgroundPixel = (maxC <= 42 && chroma <= 8);

                        if (isBackgroundPixel) {
                            isBg[x, y] = true;
                            destBytes[idx + 3] = 0; // Transparent

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

                    // Soft antialiasing / feathering on boundary
                    for (int y = 1; y < h - 1; y++) {
                        for (int x = 1; x < w - 1; x++) {
                            if (!isBg[x, y]) {
                                // Count neighboring background pixels
                                int bgNeighbors = 0;
                                for (int i = 0; i < 4; i++) {
                                    if (isBg[x + dx[i], y + dy[i]]) bgNeighbors++;
                                }
                                if (bgNeighbors > 0) {
                                    int idx = y * stride + x * 4;
                                    byte b = srcBytes[idx];
                                    byte g = srcBytes[idx + 1];
                                    byte r = srcBytes[idx + 2];
                                    int maxC = Math.Max(r, Math.Max(g, b));
                                    if (maxC < 65) {
                                        destBytes[idx + 3] = (byte)(255 - bgNeighbors * 40);
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
