import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet, Alert } from 'react-native';
import { storeData, getData, deleteData } from '../utils/storage';
import { encryptData, decryptData } from '../utils/encryption';

type Note = { id: string; content: string; encrypted: string };

const NoteScreen: React.FC = () => {
  const [note, setNote] = useState('');
  const [notes, setNotes] = useState<Note[]>([]);
  const [viewingNote, setViewingNote] = useState<string | null>(null);
  const [decryptedContent, setDecryptedContent] = useState<string | null>(null);

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    try {
      const keys = await getData('noteKeys');
      const storedPin = await getData('userPin');
      const noteList: Note[] = [];
      if (keys && storedPin) {
        const keyArray = JSON.parse(keys);
        for (const key of keyArray) {
          const encrypted = await getData(key);
          if (encrypted) {
            try {
              const decrypted = await decryptData(encrypted, storedPin || undefined);
              noteList.push({ id: key, content: decrypted, encrypted });
            } catch (error) {
              console.error('Decryption error for note', key, ':', error);
              noteList.push({ id: key, content: encrypted, encrypted }); // Store as unencrypted if decryption fails
            }
          }
        }
      }
      setNotes(noteList);
    } catch (error) {
      console.error('Load notes error:', error);
      Alert.alert('Error', 'Failed to load notes');
    }
  };

  const saveNote = async () => {
    if (!note.trim()) {
      Alert.alert('Error', 'Note cannot be empty');
      return;
    }
    const storedPin = await getData('userPin');
    if (!storedPin) {
      Alert.alert('Error', 'No PIN set. Please set a PIN in the authentication screen.');
      return;
    }
    try {
      const encrypted = await encryptData(note, storedPin);
      const key = `note_${Date.now()}`;
      await storeData(key, encrypted);
      const keys = (await getData('noteKeys')) || '[]';
      const keyArray = JSON.parse(keys);
      keyArray.push(key);
      await storeData('noteKeys', JSON.stringify(keyArray));
      setNotes([...notes, { id: key, content: note, encrypted }]);
      setNote('');
      Alert.alert('Success', 'Note saved securely');
    } catch (error) {
      console.error('Save note error:', error);
      Alert.alert(
        'Encryption Error',
        'Failed to encrypt note due to a crypto module issue. Save unencrypted note? (PIN protection still applies)',
        [
          { text: 'Cancel', style: 'cancel' },
          {
            text: 'OK',
            onPress: async () => {
              try {
                const key = `note_${Date.now()}`;
                await storeData(key, note); // Save unencrypted
                const keys = (await getData('noteKeys')) || '[]';
                const keyArray = JSON.parse(keys);
                keyArray.push(key);
                await storeData('noteKeys', JSON.stringify(keyArray));
                setNotes([...notes, { id: key, content: note, encrypted: note }]);
                setNote('');
                Alert.alert('Warning', 'Note saved unencrypted with PIN protection.');
              } catch (saveError) {
                console.error('Unencrypted save error:', saveError);
                Alert.alert('Error', 'Failed to save note');
              }
            },
          },
        ]
      );
    }
  };

  const deleteNote = async (id: string) => {
    try {
      await deleteData(id);
      const keys = (await getData('noteKeys')) || '[]';
      const keyArray = JSON.parse(keys).filter((k: string) => k !== id);
      await storeData('noteKeys', JSON.stringify(keyArray));
      setNotes(notes.filter(note => note.id !== id));
      setViewingNote(null);
      setDecryptedContent(null);
      Alert.alert('Success', 'Note deleted');
    } catch (error) {
      console.error('Delete note error:', error);
      Alert.alert('Error', 'Failed to delete note');
    }
  };

  const viewNote = async (id: string, encrypted: string) => {
    const storedPin = await getData('userPin');
    if (!storedPin) {
      Alert.alert('Error', 'No PIN set. Please set a PIN in the authentication screen.');
      return;
    }
    try {
      const decrypted = await decryptData(encrypted, storedPin);
      setViewingNote(id);
      setDecryptedContent(decrypted);
    } catch (error) {
      console.error('View note error:', error);
      setViewingNote(id);
      setDecryptedContent(encrypted); // Show unencrypted content if decryption fails
      Alert.alert('Warning', 'Note displayed unencrypted due to decryption failure.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Secure Notes</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter your note"
        value={note}
        onChangeText={setNote}
        multiline
      />
      <Button title="Save Note" onPress={saveNote} />
      {viewingNote && decryptedContent && (
        <View style={styles.decryptedView}>
          <Text style={styles.decryptedText}>Decrypted Note:</Text>
          <Text>{decryptedContent}</Text>
        </View>
      )}
      <FlatList
        data={notes}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.note}>
            <Text onPress={() => viewNote(item.id, item.encrypted)}>{item.content}</Text>
            <Button title="Delete" onPress={() => deleteNote(item.id)} />
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, padding: 10, marginBottom: 10, borderRadius: 5, minHeight: 100 },
  note: { flexDirection: 'row', justifyContent: 'space-between', padding: 10, borderBottomWidth: 1 },
  decryptedView: { padding: 10, backgroundColor: '#f0f0f0', borderRadius: 5, marginBottom: 10 },
  decryptedText: { fontWeight: 'bold' },
});

export default NoteScreen;