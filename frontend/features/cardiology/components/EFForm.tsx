"use client";
import { useState, FormEvent } from "react";
import { EchonetEFInput } from "@/features/cardiology/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

type Props = {
  onSubmit: (data: EchonetEFInput) => void;
  loading?: boolean;
};

export default function EFForm({ onSubmit, loading = false }: Props) {
  const [videoFile, setVideoFile] = useState("");

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit({ video_file: videoFile });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Ejection Fraction Prediction</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="video_file">Echo/Video File Path</Label>
            <Input
              id="video_file"
              type="text"
              value={videoFile}
              onChange={(e) => setVideoFile(e.target.value)}
              placeholder="e.g., /path/to/video.avi"
              required
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "🫀 Assess EF"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}