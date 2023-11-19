"use client"
import { useRef, useEffect, useState } from "react"
import { Button } from "@/registry/default/ui/button"
import { Checkbox } from "@/registry/default/ui/checkbox"

const DotBgStyle = {
  backgroundImage: "radial-gradient(#888888 0.75px, transparent 0)",
  backgroundSize: "24px 24px",
  backgroundPosition: "-19px -19px",
}

export default function IndexPage() {
  const visualizationImage = useRef<HTMLImageElement>(null)
  const refDebugImage = useRef<HTMLImageElement>(null)
  const [showDebug, setShowDebug] = useState(false)

  // Refresh images every 1 second
  useEffect(() => {
    const interval = setInterval(() => {
      if (refDebugImage.current) {
        refDebugImage.current.src = "/api/xiangqi/debug_frame?" + Date.now()
      }
      if (visualizationImage.current) {
        visualizationImage.current.src = "/api/xiangqi/visualization_frame?" + Date.now()
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={DotBgStyle} className="min-h-screen">
      <section className="container grid items-center gap-6 py-2">
        <img ref={visualizationImage} src="/api/xiangqi/visualization_frame" className="w-full rounded-md max-w-[500px]" />
      </section>
      <section className="container grid items-center gap-2 py-2 mt-4">
        <div className="items-top flex space-x-2">
          <Checkbox id="debug" checked={showDebug} onClick={
            () => setShowDebug(!showDebug)
          } />
          <div className="grid gap-1.5 leading-none">
            <label
              htmlFor="debug"
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Show debug images
            </label>
          </div>
        </div>
        { showDebug && <img ref={refDebugImage} src="/api/xiangqi/debug_frame" className="w-full rounded-md" /> }
      </section>
    </div>
  )
}
