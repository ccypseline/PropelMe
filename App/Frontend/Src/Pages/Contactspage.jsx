import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"

export function ContactsPage() {
  const [contacts, setContacts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchContacts() {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_BASE_URL}/api/contacts`,
          {
            credentials: "include",
          }
        )
        if (!res.ok) throw new Error("Failed to fetch contacts")
        const data = await res.json()
        setContacts(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchContacts()
  }, [])

  if (loading) return <p>Loading...</p>

  return (
    <div className="space-y-3">
      {contacts.map((c) => (
        <Card key={c.id} className="p-4 flex justify-between">
          <div>
            <p className="font-semibold">{c.name}</p>
            <p className="text-sm text-muted-foreground">{c.title}</p>
          </div>
          <div className="text-sm text-muted-foreground">{c.company}</div>
        </Card>
      ))}
    </div>
  )
}
