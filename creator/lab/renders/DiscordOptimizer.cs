using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ThunderRender {
    public class DiscordOptimizer {
        public static void Optimize(string inputPath, string outputPath, float contrast, float sharpness) {
            using (Bitmap src = new Bitmap(inputPath)) {
                int targetW = 1138;
                int targetH = 640;

                using (Bitmap resized = new Bitmap(targetW, targetH, PixelFormat.Format32bppArgb)) {
                    resized.SetResolution(96, 96);
                    using (Graphics g = Graphics.FromImage(resized)) {
                        g.InterpolationMode = InterpolationMode.HighQualityBicubic;
                        g.SmoothingMode = SmoothingMode.HighQuality;
                        g.PixelOffsetMode = PixelOffsetMode.HighQuality;
                        g.CompositingQuality = CompositingQuality.HighQuality;
                        g.DrawImage(src, new Rectangle(0, 0, targetW, targetH), 0, 0, src.Width, src.Height, GraphicsUnit.Pixel);
                    }

                    BitmapData bmpData = resized.LockBits(new Rectangle(0, 0, targetW, targetH), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
                    int stride = bmpData.Stride;
                    int bytes = stride * targetH;
                    byte[] rgb = new byte[bytes];
                    byte[] res = new byte[bytes];
                    Marshal.Copy(bmpData.Scan0, rgb, 0, bytes);
                    Array.Copy(rgb, res, bytes);

                    // 1. Sharpening filter
                    for (int y = 1; y < targetH - 1; y++) {
                        int rowPrev = (y - 1) * stride;
                        int rowCurr = y * stride;
                        int rowNext = (y + 1) * stride;

                        for (int x = 1; x < targetW - 1; x++) {
                            int idx = rowCurr + x * 4;
                            for (int c = 0; c < 3; c++) {
                                int center = rgb[idx + c];
                                int up = rgb[rowPrev + x * 4 + c];
                                int down = rgb[rowNext + x * 4 + c];
                                int left = rgb[rowCurr + (x - 1) * 4 + c];
                                int right = rgb[rowCurr + (x + 1) * 4 + c];

                                int lap = (center * 4) - (up + down + left + right);
                                int val = (int)(center + lap * sharpness);

                                // 2. Contrast enhancement
                                // val between 0 and 255 centered around 128
                                double normalized = (val - 128.0) / 128.0;
                                double contrasted = normalized * contrast;
                                int finalVal = (int)(contrasted * 128.0 + 128.0);

                                if (finalVal < 0) finalVal = 0;
                                if (finalVal > 255) finalVal = 255;
                                res[idx + c] = (byte)finalVal;
                            }
                        }
                    }

                    Marshal.Copy(res, 0, bmpData.Scan0, bytes);
                    resized.UnlockBits(bmpData);

                    ImageCodecInfo jpegCodec = null;
                    foreach (var codec in ImageCodecInfo.GetImageEncoders()) {
                        if (codec.MimeType == "image/jpeg") {
                            jpegCodec = codec;
                            break;
                        }
                    }
                    EncoderParameters p = new EncoderParameters(1);
                    p.Param[0] = new EncoderParameter(Encoder.Quality, 98L);
                    resized.Save(outputPath, jpegCodec, p);
                }
            }
        }
    }
}
