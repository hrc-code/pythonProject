const CryptoJS = require("crypto-js");

function encryptAES_CBC(plainText, key, iv) {
    try {
        // 生成一个16字节的随机IV
        // const iv = CryptoJS.lib.WordArray.random(16);

        // 使用CBC模式和PKCS7填充进行加密
        const cipherParams = CryptoJS.AES.encrypt(plainText, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });

        // 将IV附加到密文前面，以逗号分隔
        let result = iv.toString(CryptoJS.enc.Hex) + ',' + cipherParams.ciphertext.toString(CryptoJS.enc.Hex);
        return cipherParams.ciphertext.toString(CryptoJS.enc.Hex)
    } catch (error) {
        console.error("Encryption error:", error);
        throw error;
    }
}

function decryptAES_CBC(cipherTextWithIv, key, iv) {
    try {
        // 分割字符串以获取IV和密文
        // const parts = cipherTextWithIv.split(',');
        // if (parts.length !== 2) throw new Error('Invalid ciphertext format');

        // 将IV和密文转换为WordArray对象
        // const iv = CryptoJS.enc.Hex.parse(parts[0]);
        const ciphertext = CryptoJS.enc.Hex.parse(parts[1]);

        // 创建cipherParams对象
        const cipherParams = CryptoJS.lib.CipherParams.create({
            ciphertext: ciphertext
        });

        // 使用CBC模式和PKCS7填充进行解密
        const decrypted = CryptoJS.AES.decrypt(cipherParams, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });

        return decrypted.toString(CryptoJS.enc.Utf8);
    } catch (error) {
        console.error("Decryption error:", error);
        throw error;
    }
}

function encryptAES_ECB(plainText, key) {
    try {
        // 将key转换为WordArray以确保正确的长度和格式
        const keyWordArray = CryptoJS.enc.Utf8.parse(key);
        plainText = CryptoJS.enc.Utf8.parse(plainText);
        // 使用 ECB 模式和 PKCS7 填充进行加密
        const cipher = CryptoJS.AES.encrypt(
            plainText,
            keyWordArray,
            {
                mode: CryptoJS.mode.ECB,
                padding: CryptoJS.pad.Pkcs7,
                iv: undefined // ECB 模式不需要 IV
            }
        );

        return cipher.toString();
    } catch (error) {
        console.error("Encryption error:", error);
        throw error;
    }
}

function decryptAES_ECB(cipherText, key) {
    try {
        // 使用 ECB 模式和 PKCS7 填充进行解密
        const bytes = CryptoJS.AES.decrypt(cipherText, key, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7,
            iv: undefined // ECB 模式不需要 IV
        });

        return bytes.toString(CryptoJS.enc.Utf8);
    } catch (error) {
        console.error("Decryption error:", error);
        throw error;
    }
}

function test() {
    return encryptAES_ECB("Hello, World!", "")
}



