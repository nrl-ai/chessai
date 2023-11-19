import { Button } from "@/registry/default/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/registry/default/ui/card"
import { Skeleton } from "@/registry/default/ui/skeleton"

export function AppTemplate() {
  return (
    <Card className="rounded-md border border-gray-600 shadow-sm">
      <CardHeader className="grid grid-cols-[1fr_110px] items-start gap-4 space-y-0">
        <div className="space-y-1">
          <Skeleton className="h-[32px] w-[150px] rounded-md" />
          <Skeleton className="h-[32px] w-[200px] rounded-md" />
        </div>
        <Skeleton />
      </CardHeader>
      <CardContent></CardContent>
    </Card>
  )
}
