
interface UseFilePickerOptions {
    onFileSelect: (content: string) => void;
    accept?: string;
}

export function useFilePicker({ onFileSelect, accept = "text/markdown" }: UseFilePickerOptions) {
    const openFilePicker = () => {
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = accept;
        fileInput.style.display = "none";
        document.body.appendChild(fileInput);

        fileInput.addEventListener("change", (event) => {
            const input = event.target as HTMLInputElement;
            const file = input.files?.[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    if (e.target?.result) {
                        onFileSelect(e.target.result as string);
                    }
                };
                reader.readAsText(file);
            }
            document.body.removeChild(fileInput); // 使用后移除
        });

        fileInput.click();
    };

    return openFilePicker;
}
