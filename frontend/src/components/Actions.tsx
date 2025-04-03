interface ActionsProps {
    onDownloadPdf: () => void;
    onEmpty: () => void;
    onPaste: () => void;
    onUpload: () => void;
    loading: boolean;
    showEmpty: boolean;
}

export default function Actions({ onDownloadPdf, onEmpty, onPaste, onUpload, loading, showEmpty }: ActionsProps) {
    return (
        <div className="navbar bg-base-200 shadow-sm">
            <div className="navbar-start">
                <a className="btn btn-ghost text-xl">Markdown To Pdf</a>
            </div>
            <div className="navbar-end">
                <div className="tooltip tooltip-bottom" data-tip="Empty">
                    {showEmpty && (
                        <button className="btn btn-ghost btn-circle mr-2.5" onClick={onEmpty}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-circle-x-icon lucide-circle-x"><circle cx="12" cy="12" r="10" /><path d="m15 9-6 6" /><path d="m9 9 6 6" /></svg>
                        </button>
                    )}
                </div>
                <div className="tooltip tooltip-bottom" data-tip="Paste">
                    <button className="btn btn-ghost btn-circle mr-2.5" onClick={onPaste}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-clipboard-copy-icon lucide-clipboard-copy"><rect width="8" height="4" x="8" y="2" rx="1" ry="1" /><path d="M8 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" /><path d="M16 4h2a2 2 0 0 1 2 2v4" /><path d="M21 14H11" /><path d="m15 10-4 4 4 4" /></svg>
                    </button>
                </div>
                <div className="tooltip tooltip-bottom" data-tip="Upload">
                    <button className="btn btn-ghost btn-circle mr-6" onClick={onUpload}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-upload-icon lucide-upload"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" x2="12" y1="3" y2="15" /></svg>
                    </button>
                </div>
                <button disabled={loading || !showEmpty} className="btn btn-primary w-35" onClick={onDownloadPdf}>
                    {loading ? <>Loading <span className="loading loading-spinner loading-xs"></span></> : "Download Pdf"}
                </button>
            </div>
        </div >
    );
}