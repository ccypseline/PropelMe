cat > src/App.jsx << 'EOF'
import { Routes, Route, Navigate } from "react-router-dom"
import { Layout } from "./components/layout/Layout"
import { DashboardPage } from "./pages/DashboardPage"
import { ContactsPage } from "./pages/ContactsPage"

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <Layout>
            <DashboardPage />
          </Layout>
        }
      />
      <Route
        path="/contacts"
        element={
          <Layout>
            <ContactsPage />
          </Layout>
        }
      />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default App
EOF
