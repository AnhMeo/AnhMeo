import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

type Props = { navigation: any };

const HomeScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to CatVault</Text>
      <Button title="Create Note" onPress={() => navigation.navigate('Notes')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
});

export default HomeScreen;