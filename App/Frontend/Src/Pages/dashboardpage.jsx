import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function DashboardPage() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card className="p-4">
        <h2 className="font-semibold mb-1">This week</h2>
        <p className="text-sm text-muted-foreground">
          High-level summary of your networking & outreach.
        </p>
        <div className="mt-4 flex gap-2">
          <Badge>3 warm leads</Badge>
          <Badge variant="outline">2 intros pending</Badge>
        </div>
      </Card>

      <Card className="p-4">
        <h2 className="font-semibold mb-1">Upcoming tasks</h2>
        <p className="text-sm text-muted-foreground">
          Pull from backend /weekly-plan later.
        </p>
      </Card>

      <Card className="p-4">
        <h2 className="font-semibold mb-1">AI insights</h2>
        <p className="text-sm text-muted-foreground">
          This will call Vertex AI via your backend.
        </p>
      </Card>
    </div>
  )
}
