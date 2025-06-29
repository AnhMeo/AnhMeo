import * as SecureStore from 'expo-secure-store';

export const storeData = async (key: string, value: string): Promise<void> => {
  try {
    await SecureStore.setItemAsync(key, value, {
      keychainAccessible: SecureStore.WHEN_UNLOCKED, // Use WHEN_UNLOCKED for no biometrics
    });
  } catch (error) {
    console.error('Storage error:', error);
    throw error;
  }
};

export const getData = async (key: string): Promise<string | null> => {
  try {
    return await SecureStore.getItemAsync(key, {
      keychainAccessible: SecureStore.WHEN_UNLOCKED, // Use WHEN_UNLOCKED for no biometrics
    });
  } catch (error) {
    console.error('Retrieval error:', error);
    throw error;
  }
};

export const deleteData = async (key: string): Promise<void> => {
  try {
    await SecureStore.deleteItemAsync(key, {
      keychainAccessible: SecureStore.WHEN_UNLOCKED, // Use WHEN_UNLOCKED for no biometrics
    });
  } catch (error) {
    console.error('Deletion error:', error);
    throw error;
  }
};