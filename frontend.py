import React, { useState, useEffect } from 'react';
import { Book, Award, TrendingUp, LogOut, User, Code, Zap, Star, Trophy, Target, Clock } from 'lucide-react';

// Mock API Service
const api = {
  async login(username, password) {
    return {
      access: 'mock_token_' + Date.now(),
      user: {
        id: 1,
        username,
        email: `${username}@example.com`,
        role: 'student',
        age: 10,
        points: 150,
        level: 3
      }
    };
  },
  
  async register(data) {
    return { success: true, user: data };
  },
  
  async getCourses() {
    return [
      { id: 1, title: 'Podstawy Scratch', description: 'Naucz się tworzyć gry i animacje', difficulty: 'beginner', icon: 'code', color: 'blue', lesson_count: 12 },
      { id: 2, title: 'Python dla Dzieci', description: 'Pierwsze kroki w programowaniu', difficulty: 'beginner', icon: 'zap', color: 'yellow', lesson_count: 15 },
      { id: 3, title: 'HTML & CSS', description: 'Twórz własne strony internetowe', difficulty: 'intermediate', icon: 'star', color: 'purple', lesson_count: 10 },
      { id: 4, title: 'JavaScript dla Młodych', description: 'Dodaj interaktywność do stron', difficulty: 'intermediate', icon: 'trophy', color: 'green', lesson_count: 18 }
    ];
  },
  
  async getLessons(courseId) {
    return [
      { id: 1, course: courseId, title: 'Czym jest programowanie?', content: 'Wprowadzenie do świata kodowania', order: 1, points: 10, duration_minutes: 15 },
      { id: 2, course: courseId, title: 'Twój pierwszy kod', content: 'Napisz swój pierwszy program', order: 2, points: 15, duration_minutes: 20 },
      { id: 3, course: courseId, title: 'Pętle i warunki', content: 'Poznaj podstawowe struktury', order: 3, points: 20, duration_minutes: 25 }
    ];
  },
  
  async getStats() {
    return {
      completed_lessons: 8,
      total_points: 150,
      achievements: 3,
      level: 3
    };
  }
};

const LoginPage = ({ onLogin, onSwitchToRegister }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!username || !password) return;
    setLoading(true);
    try {
      const data = await api.login(username, password);
      onLogin(data);
    } catch (error) {
      alert('Błąd logowania');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mb-4">
            <Code className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">KodKids</h1>
          <p className="text-gray-600">Platforma programowania dla dzieci</p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Nazwa użytkownika</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Wpisz swoją nazwę"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hasło</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Wpisz hasło"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50"
          >
            {loading ? 'Logowanie...' : 'Zaloguj się'}
          </button>
        </div>

        <div className="mt-6 text-center">
          <button
            onClick={onSwitchToRegister}
            className="text-blue-500 hover:text-blue-700 font-medium"
          >
            Nie masz konta? Zarejestruj się!
          </button>
        </div>
      </div>
    </div>
  );
};

const RegisterPage = ({ onRegister, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    age: ''
  });

  const handleSubmit = async () => {
    if (!formData.username || !formData.email || !formData.password || !formData.age) {
      alert('Proszę wypełnić wszystkie pola');
      return;
    }
    await api.register(formData);
    onRegister();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 via-teal-500 to-blue-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Dołącz do KodKids!</h1>
          <p className="text-gray-600">Zacznij swoją przygodę z programowaniem</p>
        </div>

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Nazwa użytkownika"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            onChange={(e) => setFormData({...formData, username: e.target.value})}
          />
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            onChange={(e) => setFormData({...formData, email: e.target.value})}
          />
          <input
            type="password"
            placeholder="Hasło"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            onChange={(e) => setFormData({...formData, password: e.target.value})}
          />
          <input
            type="number"
            placeholder="Wiek (5-18 lat)"
            min="5"
            max="18"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            onChange={(e) => setFormData({...formData, age: e.target.value})}
          />
          <button
            onClick={handleSubmit}
            className="w-full bg-gradient-to-r from-green-500 to-teal-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all"
          >
            Zarejestruj się
          </button>
        </div>

        <div className="mt-6 text-center">
          <button onClick={onSwitchToLogin} className="text-green-500 hover:text-green-700 font-medium">
            Masz już konto? Zaloguj się!
          </button>
        </div>
      </div>
    </div>
  );
};

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState('courses');
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const coursesData = await api.getCourses();
    const statsData = await api.getStats();
    setCourses(coursesData);
    setStats(statsData);
  };

  const handleSelectCourse = async (course) => {
    setSelectedCourse(course);
    const lessonsData = await api.getLessons(course.id);
    setLessons(lessonsData);
    setActiveTab('lessons');
  };

  const StatCard = ({ icon: Icon, title, value, color }) => (
    <div className={`bg-gradient-to-br ${color} rounded-2xl p-6 text-white shadow-lg`}>
      <div className="flex items-center justify-between mb-2">
        <Icon className="w-8 h-8" />
        <span className="text-3xl font-bold">{value}</span>
      </div>
      <p className="text-sm opacity-90">{title}</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <Code className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-800">KodKids</h1>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 bg-yellow-100 px-4 py-2 rounded-full">
              <Star className="w-5 h-5 text-yellow-600" />
              <span className="font-semibold text-yellow-700">{user.points} punktów</span>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="font-semibold text-gray-800">{user.username}</p>
                <p className="text-xs text-gray-500">Poziom {user.level}</p>
              </div>
              <button
                onClick={onLogout}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <LogOut className="w-5 h-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard icon={Book} title="Ukończone lekcje" value={stats.completed_lessons} color="from-blue-500 to-blue-600" />
            <StatCard icon={Trophy} title="Zdobyte punkty" value={stats.total_points} color="from-yellow-500 to-orange-500" />
            <StatCard icon={Award} title="Osiągnięcia" value={stats.achievements} color="from-purple-500 to-pink-500" />
            <StatCard icon={TrendingUp} title="Poziom" value={stats.level} color="from-green-500 to-teal-500" />
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm mb-6 p-2 flex space-x-2">
          <button
            onClick={() => setActiveTab('courses')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${
              activeTab === 'courses'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Book className="w-5 h-5 inline mr-2" />
            Kursy
          </button>
          <button
            onClick={() => setActiveTab('lessons')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${
              activeTab === 'lessons'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Target className="w-5 h-5 inline mr-2" />
            Lekcje
          </button>
          <button
            onClick={() => setActiveTab('progress')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${
              activeTab === 'progress'
                ? 'bg-blue-500 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <TrendingUp className="w-5 h-5 inline mr-2" />
            Postępy
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          {activeTab === 'courses' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Dostępne kursy</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {courses.map((course) => (
                  <div
                    key={course.id}
                    onClick={() => handleSelectCourse(course)}
                    className="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all cursor-pointer hover:scale-105"
                  >
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-blue-600 rounded-lg flex items-center justify-center mb-4">
                      <Code className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-800 mb-2">{course.title}</h3>
                    <p className="text-gray-600 text-sm mb-4">{course.description}</p>
                    <div className="flex items-center justify-between text-sm">
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
                        {course.difficulty === 'beginner' ? 'Początkujący' : 'Średniozaawansowany'}
                      </span>
                      <span className="text-gray-500">{course.lesson_count} lekcji</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'lessons' && (
            <div>
              <div className="mb-6">
                {selectedCourse ? (
                  <>
                    <button
                      onClick={() => setActiveTab('courses')}
                      className="text-blue-500 hover:text-blue-700 mb-4 flex items-center"
                    >
                      ← Powrót do kursów
                    </button>
                    <h2 className="text-2xl font-bold text-gray-800">{selectedCourse.title}</h2>
                    <p className="text-gray-600 mt-2">{selectedCourse.description}</p>
                  </>
                ) : (
                  <p className="text-gray-500">Wybierz kurs, aby zobaczyć lekcje</p>
                )}
              </div>

              {lessons.length > 0 && (
                <div className="space-y-4">
                  {lessons.map((lesson, index) => (
                    <div key={lesson.id} className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-all">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-600 rounded-full font-bold text-sm">
                              {index + 1}
                            </span>
                            <h3 className="text-lg font-semibold text-gray-800">{lesson.title}</h3>
                          </div>
                          <p className="text-gray-600 text-sm mb-3 ml-11">{lesson.content}</p>
                          <div className="flex items-center space-x-4 ml-11 text-sm text-gray-500">
                            <div className="flex items-center">
                              <Clock className="w-4 h-4 mr-1" />
                              {lesson.duration_minutes} min
                            </div>
                            <div className="flex items-center">
                              <Star className="w-4 h-4 mr-1 text-yellow-500" />
                              {lesson.points} punktów
                            </div>
                          </div>
                        </div>
                        <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                          Rozpocznij
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'progress' && stats && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Twoje postępy</h2>
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6">
                  <h3 className="font-semibold text-gray-800 mb-4">Ogólne statystyki</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-gray-600 text-sm">Ukończone lekcje</p>
                      <p className="text-3xl font-bold text-blue-600">{stats.completed_lessons}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Zdobyte punkty</p>
                      <p className="text-3xl font-bold text-purple-600">{stats.total_points}</p>
                    </div>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-xl p-6">
                  <h3 className="font-semibold text-gray-800 mb-4">Poziom postępu</h3>
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="text-gray-600">Poziom {stats.level}</span>
                    <span className="text-gray-600">{stats.total_points} / {stats.level * 100} pkt</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full transition-all"
                      style={{ width: `${(stats.total_points % 100)}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = (data) => {
    setUser(data.user);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
  };

  const handleRegister = () => {
    setShowRegister(false);
  };

  if (!isLoggedIn) {
    return showRegister ? (
      <RegisterPage onRegister={handleRegister} onSwitchToLogin={() => setShowRegister(false)} />
    ) : (
      <LoginPage onLogin={handleLogin} onSwitchToRegister={() => setShowRegister(true)} />
    );
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}