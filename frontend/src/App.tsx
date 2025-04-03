import { markdown, markdownLanguage } from '@codemirror/lang-markdown';
import { languages } from '@codemirror/language-data';
import CodeMirror from '@uiw/react-codemirror';
import { useCallback, useReducer } from "react";
import Actions from "./components/Actions";
import Alert from './components/Alert';
import { downloadFileWithFormPost } from './http/down';
import { useFilePicker } from './utils/common';

// Define state type
interface State {
  code: string;
  loading: boolean;
  error: string | null;
}

// Define action types
type Action =
  | { type: 'SET_CODE'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };

// Initial state
const initialState: State = {
  code: "# markdown to pdf",
  loading: false,
  error: null,
};

// Reducer function
const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'SET_CODE':
      return { ...state, code: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export default function App() {
  const [state, dispatch] = useReducer(reducer, initialState);

  // Handle code changes
  const onChange = useCallback((val: string) => {
    dispatch({ type: 'SET_CODE', payload: val });
  }, []);

  // Handle PDF download
  const onDownloadPdf = useCallback(async () => {
    if (state.loading) return; // Prevent multiple requests
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      await downloadFileWithFormPost(
        'http://127.0.0.1:8882/api/topdf',
        { mdcontent: state.code },
        'output.pdf'
      );
    } catch (error) {
      console.error("PDF download failed:", error);
      dispatch({ type: 'SET_ERROR', payload: error instanceof Error ? error.message : String(error) });

      setTimeout(() => {
        dispatch({ type: 'SET_ERROR', payload: null });
      }, 1500);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [state.code, state.loading]);

  const onEmpty = useCallback(() => {
    dispatch({ type: 'SET_CODE', payload: "" });
  }, []);

  const onPaste = useCallback(async () => {
    const text = await navigator.clipboard.readText();
    dispatch({ type: 'SET_CODE', payload: text });
  }, []);

  const openFilePicker = useFilePicker({
    onFileSelect: (content: string) => dispatch({ type: "SET_CODE", payload: content }),
  });

  const onUpload = () => {
    openFilePicker()
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col">
      <Actions onDownloadPdf={onDownloadPdf} onEmpty={onEmpty} onPaste={onPaste} onUpload={onUpload} loading={state.loading} showEmpty={state.code.trim() !== ""} />

      {state.error && <Alert errorMessage={state.error}></Alert>}

      <div className='flex-grow'>
        <CodeMirror
          value={state.code}
          editable={!state.loading}
          onChange={onChange}
          minHeight="500px"
          extensions={[markdown({ base: markdownLanguage, codeLanguages: languages })]}
        />
      </div>
    </div>
  );
}
