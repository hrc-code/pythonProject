// const axios = require('axios')
// // 以前的逻辑
// function login(userAccount, userPassword) {
//     let host = 'http://jwxt.hut.edu.cn'
//     var strUrl = host + "/jsxsd/Logon.do?method=logon&flag=sess";
//     let encode = ''
//     axios.post(strUrl).then(response => {
//         let dataStr = response.data
//         console.log(dataStr);
//         //         if (dataStr == "no") {
//         //             return false;
//         //         } else {
//         //             var scode = dataStr.split("#")[0];
//         //             var sxh = dataStr.split("#")[1];
//         //
//         //             var code = userAccount + "%%%" + userPassword;
//         //             for (var i = 0; i < code.length; i++) {
//         //                 if (i < 20) {
//         //                     encoded = encoded + code.substring(i, i + 1) + scode.substring(0, parseInt(sxh.substring(i, i + 1)));
//         //                     scode = scode.substring(parseInt(sxh.substring(i, i + 1)), scode.length);
//         //                 } else {
//         //                     encoded = encoded + code.substring(i, code.length);
//         //                     i = code.length;
//         //                 }
//         //             }
//         //         }
//     })
//
//     return encode
// }

//Base64 编码 浏览器
function encodeInp(input) {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    do {
        chr1 = input.charCodeAt(i++);
        chr2 = input.charCodeAt(i++);
        chr3 = input.charCodeAt(i++);

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }

        output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) + keyStr.charAt(enc3) + keyStr.charAt(enc4);
        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = "";

    } while (i < input.length);

    return output;
}

// node base64
function encodeBase64(input) {
    // 创建 Buffer 并使用 'base64' 编码转换为 Base64 字符串
    return Buffer.from(input).toString('base64');
}

// 拿到盐
// function getSalt() {
//
// }

// 现在的登录
function submitForm1(userAccount,userPassword, scode, sxh) {
    let encode_result = ''
    try {
        var xh = userAccount
        var pwd = userPassword

        var account = encodeBase64(xh);

        var passwd = encodeBase64(pwd);
        var code = account + "%%%" + passwd;
        var encoded = "";
        for (var i = 0; i < code.length; i++) {
            if (i < 20) {
                encoded = encoded + code.substring(i, i + 1) + scode.substring(0, parseInt(sxh.substring(i, i + 1)));
                scode = scode.substring(parseInt(sxh.substring(i, i + 1)), scode.length);
            } else {
                encoded = encoded + code.substring(i, code.length);
                i = code.length;
            }
        }
        encode_result = encoded;
        return encode_result;
    } catch (e) {
        console.log(e);
        console.log("登录失败")
        return 0;
    }
}

const encode = submitForm1('22408000511','hrcHRC123!','65p1Thwe5p509723J2624HT059ItVZon0U7XoRo042cE','32211331331332331321');
console.log(encode);

const browser_encode = 'M65pj1TIhw0eM5Dp50g972w3MJ26D24HAT1059MItVTZoEn0U=7Xo%R%o04%2caEHJjSFJDMTIzIQ=='
console.log(encode===browser_encode)