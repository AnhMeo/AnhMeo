import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import * as LocalAuthentication from 'expo-local-authentication';
import { getData } from './utils/storage';
import AuthScreen from './screens/AuthScreen';
import HomeScreen from './screens/HomeScreen';
import NoteScreen from './screens/NoteScreen';

// App.tsx
const Tab = createBottomTabNavigator();

export default function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const storedPin = await getData('userPin');
        if (!storedPin) {
          setAuthenticated(false); // Force auth screen for new users to set PIN
        } else {
          const hasHardware = await LocalAuthentication.hasHardwareAsync();
          const isEnrolled = await LocalAuthentication.isEnrolledAsync();
          if (hasHardware && isEnrolled) {
            const result = await LocalAuthentication.authenticateAsync({
              promptMessage: 'Authenticate to access CatVault',
              fallbackLabel: 'Use PIN',
            });
            setAuthenticated(result.success);
          } else {
            setAuthenticated(false); // Force PIN verification on emulator
          }
        }
      } catch (error) {
        console.error('Auth check error:', error);
        setAuthenticated(false); // Force auth screen on error
      } finally {
        setCheckingAuth(false);
      }
    };
    checkAuth();
  }, []);

  if (checkingAuth) return null;

  return (
    <NavigationContainer>
      {authenticated ? (
        <Tab.Navigator>
          <Tab.Screen name="Home" component={HomeScreen} />
          <Tab.Screen name="Notes" component={NoteScreen} />
        </Tab.Navigator>
      ) : (
        <AuthScreen onAuthSuccess={() => setAuthenticated(true)} />
      )}
    </NavigationContainer>
  );
}