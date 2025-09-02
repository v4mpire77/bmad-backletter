export default function UploadPage() {
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Upload a contract</h1>
      <p className="text-sm text-muted-foreground">
        Drop a file to create a new analysis. (Hook up to /api/uploads next.)
      </p>
      {/* TODO: Dropzone + POST /api/uploads */}
      <div className="rounded-2xl border p-8 text-center">Dropzone placeholder</div>
    </div>
  );
}
