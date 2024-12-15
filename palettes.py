# -*- coding: utf-8 -*-
# colors.py

def hex_to_rgb(hex_str):
    hex_str = hex_str.replace('#', '')
    return (int(hex_str[0:2],16), int(hex_str[2:4],16), int(hex_str[4:6],16))

#Matplotlib color gradients
class ColorDict:


    color_dict = {
        "magenta-blue":[hex_to_rgb(color) for color in ["d9ed92","b5e48c","99d98c","76c893","52b69a","34a0a4","168aad","1a759f","1e6091","184e77"]],
        "autumn":[hex_to_rgb(color) for color in ["001219","005f73","0a9396","94d2bd","e9d8a6","ee9b00","ca6702","bb3e03","ae2012","9b2226"]],
        "greys":[hex_to_rgb(color) for color in ["f8f9fa","e9ecef","dee2e6","ced4da","adb5bd","6c757d","495057","343a40","212529"]],
        "fire":[hex_to_rgb(color) for color in ["03071e","370617","6a040f","9d0208","d00000","dc2f02","e85d04","f48c06","faa307","ffba08"]],
        "blues":[hex_to_rgb(color) for color in ["0f3375","13459c","1557c0","196bde","2382f7","4b9cf9","77b6fb","a4cefc","cce4fd","e8f3fe"]],
        "darkblues":[hex_to_rgb(color) for color in ["00111c","001523","001a2c","002137","00253e","002945","002e4e","003356","003a61","00406c"]],
        "greyblues":[hex_to_rgb(color) for color in ["0466c8","0353a4","023e7d","002855","001845","001233","33415c","5c677d","7d8597","979dac"]],
        "purples":[hex_to_rgb(color) for color in ["10002b","240046","3c096c","5a189a","7b2cbf","9d4edd","c77dff","e0aaff"]],
        "rainbow":[hex_to_rgb(color) for color in ["ff0000","ff8700","ffd300","deff0a","a1ff0a","0aff99","0aefff","147df5","580aff","be0aff"]],
        "pastels":[hex_to_rgb(color) for color in ["d8e2dc","ffe5d9","ffcad4","f4acb7","9d8189","70d6ff","ff70a6","ff9770","ffd670","e9ff70"]],
        "pastels2":[hex_to_rgb(color) for color in ["9b5de5","b15dd9","c65ccd","f15bb5","f8a07b","fee440","7fd09d","00bbf9","00d8e7","00f5d4"]],
        "pastels3":[hex_to_rgb(color) for color in ["e2e2df","d2d2cf","e2cfc4","f7d9c4","faedcb","c9e4de","c6def1","dbcdf0","f2c6de","f9c6c9"]],
        "pastels4":[hex_to_rgb(color) for color in ["f992ad","fbbcee","fab4c8","f78ecf","cfb9f7","e0cefd","a480f2","d4b0f9","c580ed","d199f1"]],
        "pastels5":[hex_to_rgb(color) for color in ["fbf8cc","fde4cf","ffcfd2","f1c0e8","cfbaf0","a3c4f3","90dbf4","8eecf5","98f5e1","b9fbc0"]],
        "blue-purple":[hex_to_rgb(color) for color in ["2d00f7","6a00f4","8900f2","a100f2","b100e8","bc00dd","d100d1","db00b6","e500a4","f20089"]],
        "not-sure":[hex_to_rgb(color) for color in ["090c02","7765e3","fcfcfc","0a014f","605f5e","f8f8f8","d2d6ef","e6e6e6"]],
        "sunset":[hex_to_rgb(color) for color in ["ffbe0b","fd8a09","fb5607","fd2b3b","ff006e","c11cad","8338ec","5f5ff6","4d73fb","3a86ff"]],
        "orange-purple":[hex_to_rgb(color) for color in ["ff6d00","ff7900","ff8500","ff9100","ff9e00","240046","3c096c","5a189a","7b2cbf","9d4edd"]],
        "darkgreenpurple":[hex_to_rgb(color) for color in ["006466","065a60","0b525b","144552","1b3a4b","212f45","272640","312244","3e1f47","4d194d"]],
        "variations":[hex_to_rgb(color) for color in ["006699","ffcc00","ff9900","669900","99cc33","cc3399","3399cc","ff6600","990066","ccee66"]],
        "variations2":[hex_to_rgb(color) for color in ["262626","7a0213","00193a","131313","023f73","bf0a26","034780","002b53","a10220","cd0c2b"]],
        "variations3":[hex_to_rgb(color) for color in ["a24ccd","c586dd","7400b8","dcace8","9739c8","d099e3","8013bd","ae60d3","8b26c3","b973d8"]],
        "variations4":[hex_to_rgb(color) for color in ["71093b","990b52","cb8b15","eaaa34","ffffff","f1f4f9","749ed2","467ec3","023578","022450"]],
        "variations5":[hex_to_rgb(color) for color in ["c63333","f2636a","229e99","e94900","f58606","ef6803","dc4b4f","36a7a2","c1b225","72a85f"]],
        "variations6":[hex_to_rgb(color) for color in ["9d0208","dc2f02","fbb539","03071e","f48c06","e85d04","faa307","d00000","6a040f","370617"]],
    }

    def get_colornames(self):
        return list(self.color_dict.keys())

    def get_colordict(self):
        return self.color_dict