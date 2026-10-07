using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace ThunderRender {
    public class Enhancer {
        public static void Process(string inputPath, string outputPath, int targetW, int targetH, float sharpness) {
            using (Bitmap src = new Bitmap(inputPath)) {
                using (Bitmap upscaled = new Bitmap(targetW, targetH, PixelFormat.Format32bppArgb)) {
                    upscaled.SetResolution(300, 300);
                    using (Graphics g = Graphics.FromImage(upscaled)) {
                        g.InterpolationMode = InterpolationMode.HighQualityBicubic;
                        g.SmoothingMode = SmoothingMode.None;
                        g.PixelOffsetMode = PixelOffsetMode.HighQuality;
                        g.CompositingQuality = CompositingQuality.HighQuality;
                        g.DrawImage(src, new Rectangle(0, 0, targetW, targetH));
                    }

                    BitmapData bmpData = upscaled.LockBits(new Rectangle(0, 0, targetW, targetH), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
                    int stride = bmpData.Stride;
                    int bytes = stride * targetH;
                    byte[] rgb = new byte[bytes];
                    byte[] res = new byte[bytes];
                    Marshal.Copy(bmpData.Scan0, rgb, 0, bytes);
                    Array.Copy(rgb, res, bytes);

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

                                int laplacian = (center * 4) - (up + down + left + right);
                                int val = (int)(center + laplacian * sharpness);
                                if (val < 0) val = 0;
                                if (val > 255) val = 255;
                                res[idx + c] = (byte)val;
                            }
                        }
                    }

                    Marshal.Copy(res, 0, bmpData.Scan0, bytes);
                    upscaled.UnlockBits(bmpData);

                    ImageCodecInfo jpegCodec = null;
                    foreach (var codec in ImageCodecInfo.GetImageEncoders()) {
                        if (codec.MimeType == "image/jpeg") {
                            jpegCodec = codec;
                            break;
                        }
                    }
                    EncoderParameters p = new EncoderParameters(1);
                    p.Param[0] = new EncoderParameter(Encoder.Quality, 100L);
                    upscaled.Save(outputPath, jpegCodec, p);
                }
            }
        }
    }
}
