import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  RefreshControl,
  SafeAreaView,
  TouchableOpacity
} from 'react-native';
import api from '../services/api';

export default function HomeScreen() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await api.get('/analytics/dashboard/');
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadStats();
    setRefreshing(false);
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Ładowanie...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <View style={styles.header}>
          <Text style={styles.greeting}>Cześć, {stats?.user?.username}! 👋</Text>
          <Text style={styles.subheader}>Poziom {stats?.user?.level}</Text>
        </View>

        <View style={styles.statsGrid}>
          <View style={[styles.statCard, { backgroundColor: '#4F46E5' }]}>
            <Text style={styles.statValue}>{stats?.stats?.completed_lessons}</Text>
            <Text style={styles.statLabel}>Ukończone lekcje</Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: '#EC4899' }]}>
            <Text style={styles.statValue}>{stats?.user?.points}</Text>
            <Text style={styles.statLabel}>Punkty</Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: '#10B981' }]}>
            <Text style={styles.statValue}>{stats?.stats?.average_score}%</Text>
            <Text style={styles.statLabel}>Średni wynik</Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: '#F59E0B' }]}>
            <Text style={styles.statValue}>{stats?.user?.level}</Text>
            <Text style={styles.statLabel}>Poziom</Text>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Twoje kursy</Text>
          {stats?.courses?.map((course) => (
            <View key={course.course_id} style={styles.courseCard}>
              <Text style={styles.courseTitle}>{course.course_title}</Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { width: `${course.progress_percentage}%` }
                  ]} 
                />
              </View>
              <Text style={styles.progressText}>
                {course.completed_lessons} / {course.total_lessons} lekcji ({course.progress_percentage}%)
              </Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  header: {
    padding: 20,
    backgroundColor: 'white',
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#111827',
  },
  subheader: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 5,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 10,
  },
  statCard: {
    width: '48%',
    margin: '1%',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
  },
  statLabel: {
    fontSize: 14,
    color: 'white',
    marginTop: 5,
    opacity: 0.9,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#111827',
  },
  courseCard: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  courseTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 10,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#E5E7EB',
    borderRadius: 4,
    marginBottom: 5,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4F46E5',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 12,
    color: '#6B7280',
  },
});