"use client";
import { useState, FormEvent, useEffect, useRef, DragEvent } from "react";
import { EchonetEFInput } from "@/features/cardiology/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, X } from "lucide-react";

type Props = {
  onSubmit: (data: EchonetEFInput) => void;
  loading?: boolean;
  videoFile?: File | null;
};

export default function EFForm({ onSubmit, loading = false, videoFile: uploadedVideo }: Props) {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [videoURL, setVideoURL] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Create preview URL when file changes
  useEffect(() => {
    if (videoFile) {
      const url = URL.createObjectURL(videoFile);
      setVideoURL(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setVideoURL(null);
    }
  }, [videoFile]);

  // If video was uploaded and result exists, show that video
  useEffect(() => {
    if (uploadedVideo) {
      setVideoFile(uploadedVideo);
    }
  }, [uploadedVideo]);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!videoFile) return;
    onSubmit({ video_file: videoFile });
  };

  const handleFileSelect = (file: File) => {
    const validTypes = ['.avi', '.mp4', '.mpeg', '.mov', '.m4v', '.mpg'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (validTypes.includes(fileExtension)) {
      setVideoFile(file);
    } else {
      alert('Please upload a valid video file (.avi, .mp4, .mpeg, .mov, .m4v, .mpg)');
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleRemoveVideo = () => {
    setVideoFile(null);
    setVideoURL(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleBoxClick = () => {
    if (!loading) {
      fileInputRef.current?.click();
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Echocardiogram Video</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* === Drag & Drop Upload Box === */}
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={handleBoxClick}
            className={`
              relative border-2 border-dashed rounded-lg p-8 
              transition-all duration-200 
              ${loading ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}
              ${isDragging 
                ? 'border-blue-500 bg-blue-50' 
                : videoFile 
                  ? 'border-green-500 bg-green-50' 
                  : 'border-gray-300 hover:border-gray-400 bg-gray-50'
              }
              min-h-[400px] flex items-center justify-center
            `}
          >
            {!videoURL ? (
              // Upload prompt
              <div className="text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Drop your echo video here
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  or click to browse
                </p>
                <p className="text-xs text-gray-400">
                  Supported formats: AVI, MP4, MPEG, MOV, M4V, MPG
                </p>
              </div>
            ) : (
              // Video preview
              <div className="relative w-full h-full flex items-center justify-center">
                <video
                  src={videoURL}
                  controls
                  className="max-w-full max-h-[380px] rounded shadow-lg"
                  onClick={(e) => e.stopPropagation()}
                />
                {!loading && (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleRemoveVideo();
                    }}
                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 shadow-lg transition-colors"
                    aria-label="Remove video"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
            )}

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept=".avi,.mp4,.mpeg,.mov,.m4v,.mpg,video/*"
              onChange={handleInputChange}
              style={{ display: 'none' }}
              disabled={loading}
            />
          </div>

          {/* File info */}
          {videoFile && (
            <div className="text-sm text-gray-600">
              <strong>File:</strong> {videoFile.name} ({(videoFile.size / 1024 / 1024).toFixed(2)} MB)
            </div>
          )}

          <Button 
            type="submit" 
            disabled={loading || !videoFile}
            className="w-full"
          >
            {loading ? "Analyzing..." : "🫀 Predict Ejection Fraction"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}