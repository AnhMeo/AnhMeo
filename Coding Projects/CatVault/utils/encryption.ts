import * as CryptoJS from 'crypto-js';
import * as SecureStore from 'expo-secure-store';
import * as ExpoCrypto from 'expo-crypto';
import { Alert } from 'react-native';

// Fallback random bytes generation using Math.random if ExpoCrypto fails
function getFallbackRandomBytes(length: number): Uint8Array {
  const array = new Uint8Array(length);
  for (let i = 0; i < length; i++) {
    array[i] = Math.floor(Math.random() * 256);
  }
  return array;
}

export const getSecretKey = async (pin?: string): Promise<string> => {
  try {
    let key = await SecureStore.getItemAsync('encryptionKey', {
      keychainAccessible: SecureStore.WHEN_UNLOCKED,
    });
    if (key === null) {
      if (!pin) {
        throw new Error('PIN required to generate encryption key');
      }
      let randomBytes;
      try {
        randomBytes = await ExpoCrypto.getRandomBytesAsync(32); // 32 bytes for AES-256
      } catch (cryptoError) {
        console.warn('ExpoCrypto failed, using fallback random bytes:', cryptoError);
        randomBytes = getFallbackRandomBytes(32);
      }
      key = CryptoJS.enc.Hex.stringify(CryptoJS.lib.WordArray.create(randomBytes));
      await SecureStore.setItemAsync('encryptionKey', key, {
        keychainAccessible: SecureStore.WHEN_UNLOCKED,
      });
      await SecureStore.setItemAsync('userPin', pin, {
        keychainAccessible: SecureStore.WHEN_UNLOCKED,
      });
    }
    return key;
  } catch (error) {
    console.error('Key retrieval/generation error:', error);
    throw error;
  }
};

const getIV = async (): Promise<string> => {
  try {
    let randomBytes;
    try {
      randomBytes = await ExpoCrypto.getRandomBytesAsync(16); // 16 bytes for AES-CBC
    } catch (cryptoError) {
      console.warn('ExpoCrypto failed, using fallback random bytes:', cryptoError);
      randomBytes = getFallbackRandomBytes(16);
    }
    return CryptoJS.enc.Hex.stringify(CryptoJS.lib.WordArray.create(randomBytes));
  } catch (error) {
    console.error('IV generation error:', error);
    throw error;
  }
};

export const encryptData = async (data: string, pin?: string): Promise<string> => {
  try {
    const key = await getSecretKey(pin);
    const iv = await getIV();
    const encrypted = CryptoJS.AES.encrypt(data, key, { iv: CryptoJS.enc.Hex.parse(iv) }).toString();
    return iv + ':' + encrypted;
  } catch (error) {
    console.error('Encryption error:', error);
    return new Promise((resolve, reject) => {
      Alert.alert(
        'Encryption Error',
        'Failed to encrypt note due to a crypto module issue. Save unencrypted note? (PIN protection still applies)',
        [
          { text: 'Cancel', style: 'cancel', onPress: () => reject(error) },
          {
            text: 'OK',
            onPress: () => resolve(data), // Save unencrypted data
          },
        ]
      );
    });
  }
};

export const decryptData = async (encryptedData: string, pin?: string): Promise<string> => {
  try {
    const [iv, encrypted] = encryptedData.split(':');
    if (!iv || !encrypted) {
      throw new Error('Invalid encrypted data format');
    }
    const key = await getSecretKey(pin);
    const decrypted = CryptoJS.AES.decrypt(encrypted, key, { iv: CryptoJS.enc.Hex.parse(iv) }).toString(CryptoJS.enc.Utf8);
    if (!decrypted) {
      throw new Error('Decryption failed');
    }
    return decrypted;
  } catch (error) {
    console.error('Decryption error:', error);
    throw error; // Let the caller handle decryption failure
  }
};