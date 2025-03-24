import { ReactNode, createContext, useContext, useEffect, useState } from 'react'

interface AuthContextType {
  isAuthenticated: boolean
  setIsAuthenticated: (isAuthenticated: boolean) => void
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem('token'),
  )

  const login = (token: string) => {
    localStorage.setItem('token', token)
    setIsAuthenticated(true)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setIsAuthenticated(false)
  }

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (!token) {
      setIsAuthenticated(false);
    }
  },[isAuthenticated])

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, setIsAuthenticated, login, logout }}
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
