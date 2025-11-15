import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  Alert
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { LinearGradient } from 'expo-linear-gradient';
import api from '../services/api';

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Błąd', 'Wypełnij wszystkie pola');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/auth/login/', {
        username,
        password
      });

      await AsyncStorage.setItem('authToken', response.data.tokens.access);
      await AsyncStorage.setItem('user', JSON.stringify(response.data.user));

      navigation.replace('MainTabs');
    } catch (error) {
      Alert.alert('Błąd', 'Nieprawidłowe dane logowania');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={['#4F46E5', '#7C3AED', '#EC4899']}
      style={styles.container}
    >
      <SafeAreaView style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.logo}>🚀</Text>
          <Text style={styles.title}>KodKids</Text>
          <Text style={styles.subtitle}>Platforma dla młodych programistów</Text>
        </View>

        <View style={styles.form}>
          <TextInput
            style={styles.input}
            placeholder="Nazwa użytkownika"
            placeholderTextColor="#9CA3AF"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
          />

          <TextInput
            style={styles.input}
            placeholder="Hasło"
            placeholderTextColor="#9CA3AF"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <TouchableOpacity
            style={styles.button}
            onPress={handleLogin}
            disabled={loading}
          >
            <Text style={styles.buttonText}>
              {loading ? 'Logowanie...' : 'Zaloguj się'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={() => navigation.navigate('Register')}
          >
            <Text style={styles.linkText}>
              Nie masz konta? Zarejestruj się!
            </Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 50,
  },
  logo: {
    fontSize: 80,
    marginBottom: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  form: {
    width: '100%',
  },
  input: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    fontSize: 16,
  },
  button: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 15,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonText: {
    color: '#4F46E5',
    fontSize: 16,
    fontWeight: 'bold',
  },
  linkText: {
    color: 'white',
    textAlign: 'center',
    fontSize: 14,
  },
});