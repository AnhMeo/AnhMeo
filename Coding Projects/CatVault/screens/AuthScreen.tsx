import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import * as LocalAuthentication from 'expo-local-authentication';
import { storeData, getData } from '../utils/storage';
import { getSecretKey } from '../utils/encryption';

type Props = { onAuthSuccess: () => void };

const AuthScreen: React.FC<Props> = ({ onAuthSuccess }) => {
  const [pin, setPin] = useState('');
  const [isPinSet, setIsPinSet] = useState(false);
  const [biometricSupported, setBiometricSupported] = useState(false);

  useEffect(() => {
    const initialize = async () => {
      const storedPin = await getData('userPin');
      setIsPinSet(!!storedPin);
      if (!storedPin) {
        promptForPin(); // Immediately prompt for PIN setup for new users
      } else {
        const hasHardware = await LocalAuthentication.hasHardwareAsync();
        const isEnrolled = await LocalAuthentication.isEnrolledAsync();
        setBiometricSupported(hasHardware && isEnrolled);
        if (hasHardware && isEnrolled) {
          authenticateBiometric();
        } else {
          promptForPin(); // Prompt for PIN if no biometrics
        }
      }
    };
    initialize();
  }, []);

  const authenticateBiometric = async () => {
    try {
      const result = await LocalAuthentication.authenticateAsync({
        promptMessage: 'Authenticate to access CatVault',
        fallbackLabel: 'Use PIN',
        disableDeviceFallback: false,
      });
      if (result.success) {
        onAuthSuccess();
      } else {
        promptForPin();
      }
    } catch (error) {
      console.error('Biometric error:', error);
      Alert.alert('Error', 'Biometric authentication failed');
      promptForPin();
    }
  };

  const promptForPin = async () => {
    const storedPin = await getData('userPin');
    Alert.prompt(
      'Enter PIN',
      !isPinSet ? 'Please set a 4-digit PIN' : 'Please enter your PIN to proceed',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'OK',
          onPress: async (enteredPin) => {
            if (enteredPin && enteredPin.length === 4) {
              try {
                if (!isPinSet) {
                  await getSecretKey(enteredPin); // Set initial key with PIN
                  await storeData('userPin', enteredPin); // Store PIN for future use
                  Alert.alert('Success', 'PIN set successfully!');
                } else {
                  await getSecretKey(enteredPin); // Verify PIN with key access
                }
                onAuthSuccess();
              } catch (error) {
                Alert.alert('Error', 'Incorrect PIN or setup failed');
              }
            } else {
              Alert.alert('Error', 'PIN must be 4 digits');
            }
          },
        },
      ],
      'secure-text'
    );
  };

  const handlePinSubmit = async () => {
    if (pin.length !== 4) {
      Alert.alert('Error', 'PIN must be 4 digits');
      return;
    }
    try {
      if (!isPinSet) {
        await getSecretKey(pin); // Set initial key with PIN
        await storeData('userPin', pin); // Store PIN for future use
        Alert.alert('Success', 'PIN set successfully!');
        onAuthSuccess();
      } else {
        const storedPin = await getData('userPin');
        if (storedPin === pin) {
          onAuthSuccess();
        } else {
          Alert.alert('Error', 'Incorrect PIN');
          setPin('');
        }
      }
    } catch (error) {
      console.error('PIN setup error:', error);
      Alert.alert('Error', 'Failed to set PIN');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>CatVault Authentication</Text>
      <TextInput
        style={styles.input}
        placeholder={!isPinSet ? 'Set a 4-digit PIN' : 'Enter 4-digit PIN'}
        secureTextEntry
        keyboardType="numeric"
        maxLength={4}
        value={pin}
        onChangeText={setPin}
      />
      <Button title={!isPinSet ? 'Set PIN' : 'Submit PIN'} onPress={handlePinSubmit} />
      {biometricSupported && (
        <Button title="Use Biometrics" onPress={authenticateBiometric} />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, padding: 10, marginBottom: 10, borderRadius: 5 },
});

export default AuthScreen;