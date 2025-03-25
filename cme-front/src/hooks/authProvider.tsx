import { ReactNode, createContext, useContext, useEffect, useState } from 'react'

interface AuthContextType {
  isAuthenticated: boolean
  setIsAuthenticated: (isAuthenticated: boolean) => void
  login: (token: string) => void
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!sessionStorage.getItem('token'),
  )
  const [loading, setLoading] = useState(true);

  const login = (token: string) => {
    sessionStorage.setItem('token', token)
    setIsAuthenticated(true)
  }

  const logout = () => {
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('username')
    setIsAuthenticated(false)
  }

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, setIsAuthenticated, login, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
