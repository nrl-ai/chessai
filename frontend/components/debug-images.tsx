import { useEffect, useRef, useState } from "react"
import { Checkbox } from "@/registry/default/ui/checkbox"

export function DebugImages() {
  const refDebugImage = useRef<HTMLImageElement>(null)
  const [showDebug, setShowDebug] = useState(false)

  // Refresh images every 1 second
  useEffect(() => {
    const interval = setInterval(() => {
      if (refDebugImage.current) {
        refDebugImage.current.src = "/api/vision/debug_frame?" + Date.now()
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <>
      <div className="items-top flex space-x-2">
        <Checkbox
          id="debug"
          checked={showDebug}
          onClick={() => setShowDebug(!showDebug)}
        />
        <div className="grid gap-1.5 leading-none">
          <label
            htmlFor="debug"
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            Show debug images
          </label>
        </div>
      </div>
      {showDebug && (
        <img
          ref={refDebugImage}
          src="/api/vision/debug_frame"
          className="w-full rounded-md"
          width={2000}
          height={640}
          alt="Debug Images"
        />
      )}
    </>
  )
}
