mkdir -p src/components/layout
cat > src/components/layout/Layout.jsx << 'EOF'
import { Link, useLocation } from "react-router-dom"
import { cn } from "../utils/cn"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/contacts", label: "Contacts" },
]

export function Layout({ children }) {
  const location = useLocation()

  return (
    <div className="min-h-screen flex bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-white flex flex-col">
        <div className="flex items-center gap-2 p-4">
          <div className="h-8 w-8 rounded-lg bg-primary" />
          <span className="font-semibold text-lg">PropelMe</span>
        </div>
        <Separator />
        <nav className="flex-1 p-2 space-y-1">
          {navItems.map((item) => (
            <Link key={item.to} to={item.to}>
              <div
                className={cn(
                  "flex items-center px-3 py-2 rounded-md text-sm",
                  "hover:bg-muted cursor-pointer",
                  location.pathname === item.to
                    ? "bg-muted font-medium"
                    : "text-muted-foreground"
                )}
              >
                {item.label}
              </div>
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t">
          <Button className="w-full" variant="outline" size="sm">
            Logout
          </Button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col">
        <header className="h-14 border-b flex items-center justify-between px-6 bg-white">
          <h1 className="text-lg font-semibold tracking-tight">
            PropelMe Career Concierge
          </h1>
        </header>
        <section className="flex-1 p-6">{children}</section>
      </main>
    </div>
  )
}
EOF
