# color_space_conversion

# features
1. conversion between RGB and YUV444 in HDR 2020 color gamut
2. support 10bit and 12bit
3. yuv444p10le (little edian)

# refenrence
conversion matrix defined in itu rec.2020: https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2020-2-201510-I!!PDF-E.pdf
extended in rec.2100: https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2100-2-201807-I!!PDF-E.pdf
and reinterpreted for easier understanding here:https://blog.csdn.net/helimin12345/article/details/78536520

# notes
1. Supports only 2020 color gamut, conversion matrix for rec.709 and rec.601 are different and unsupported
2. 8bit not supported
