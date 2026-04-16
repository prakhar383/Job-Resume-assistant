import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Code, FileText, CheckCircle, AlertTriangle, Loader2, Copy, Download, Settings } from 'lucide-react';

function App() {
  // Form State
  const [username, setUsername] = useState('prakhar383'); // Defaulting to you
  const [jobDescription, setJobDescription] = useState('');
  
  // App State
  const [isGenerating, setIsGenerating] = useState(false);
  const [showCacheModal, setShowCacheModal] = useState(false);
  const [cachedProjects, setCachedProjects] = useState(null);
  
  // Result State
  const [result, setResult] = useState(null);

  // Template State
  const [templateCode, setTemplateCode] = useState('');
  const [isUpdatingTemplate, setIsUpdatingTemplate] = useState(false);

  // Check for cached data when the user types a username
  const handleCheckCache = () => {
    if (!username) return;
    const savedData = localStorage.getItem(`github_projects_${username}`);
    
    if (savedData && jobDescription.trim() !== '') {
      setCachedProjects(JSON.parse(savedData));
      setShowCacheModal(true); // Trigger the popup!
    } else if (jobDescription.trim() !== '') {
      // If no cache, just run the normal generation
      generateResume(false); 
    } else {
      alert("Please paste a job description first!");
    }
  };

  const handleUpdateTemplate = async () => {
    if (!templateCode.trim()) {
      alert("Please paste the LaTeX template code first!");
      return;
    }
    setIsUpdatingTemplate(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/update-template', {
        content: templateCode
      });
      if (response.data.status === 'success') {
        alert("Template successfully updated! You can now generate resumes using this template.");
        setTemplateCode('');
      }
    } catch (error) {
      console.error(error);
      if (error.response && error.response.data && error.response.data.detail) {
        alert("Template Error: " + error.response.data.detail);
      } else {
        alert("Error updating template. Check backend console or network.");
      }
    } finally {
      setIsUpdatingTemplate(false);
    }
  };

  // The main API call
  const generateResume = async (useCache = false) => {
    setShowCacheModal(false);
    setIsGenerating(true);
    setResult(null);

    try {
      // In a fully optimized version, if useCache is true, we'd send the cachedProjects 
      // directly to the backend to skip the GitHub fetch step. 
      // For now, we are hitting the main pipeline endpoint we built earlier.
      
      const response = await axios.post('http://127.0.0.1:8000/api/generate-resume', {
        job_description: jobDescription
      });

      if (response.data.status === 'success') {
        setResult({
          score: response.data.ats_score.score,
          feedback: response.data.ats_score.feedback,
          missing: response.data.ats_score.missing_keywords,
          latex: response.data.latex_code
        });
        
        // Simulate saving to cache for next time
        if (!useCache) {
           // We pretend to save the fetch for demonstration. 
           // We will connect the real github fetch endpoint later to store real data here.
           localStorage.setItem(`github_projects_${username}`, JSON.stringify([{name: "Cached Project"}]));
        }
      }
    } catch (error) {
      console.error(error);
      alert("Error generating resume. Check backend console.");
    } finally {
      setIsGenerating(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result.latex);
    alert("LaTeX copied to clipboard!");
  };

  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      
      {/* LEFT PANE: Controls */}
      <div className="w-1/2 p-8 overflow-y-auto bg-white shadow-xl z-10 flex flex-col">
        <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
          <FileText className="text-blue-600" /> AI Resume Architect
        </h1>
        <p className="text-gray-500 mb-8">Generate ATS-optimized LaTeX resumes in seconds.</p>

        <div className="space-y-6 flex-grow">
          {/* GitHub Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">GitHub Username</label>
            <div className="relative">
              <Code className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                placeholder="e.g., prakhar383"
              />
            </div>
          </div>

          {/* JD Input */}
          <div className="flex-grow flex flex-col h-48">
            <label className="block text-sm font-medium text-gray-700 mb-2">Job Description</label>
            <textarea 
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full h-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none transition-all"
              placeholder="Paste the target job description here..."
            />
          </div>

          {/* Template Input */}
          <div className="flex flex-col h-48">
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Settings className="h-4 w-4 text-gray-500" /> Update Backend Template (Optional)
            </label>
            <textarea 
              value={templateCode}
              onChange={(e) => setTemplateCode(e.target.value)}
              className="w-full h-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-800 focus:border-gray-800 outline-none resize-none transition-all text-xs font-mono bg-gray-50"
              placeholder="Paste raw LaTeX here. Must contain {{DYNAMIC_OBJECTIVE_PLACEHOLDER}} and {{DYNAMIC_PROJECTS_PLACEHOLDER}}"
            />
            <button 
              onClick={handleUpdateTemplate}
              disabled={isUpdatingTemplate || !templateCode.trim()}
              className="mt-2 w-full bg-gray-800 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 text-sm"
            >
              {isUpdatingTemplate ? <Loader2 className="animate-spin h-4 w-4" /> : <Settings className="h-4 w-4" />}
              {isUpdatingTemplate ? "Updating Template..." : "Overwrite Template"}
            </button>
          </div>
        </div>

        <button 
          onClick={handleCheckCache}
          disabled={isGenerating}
          className="mt-8 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50"
        >
          {isGenerating ? <Loader2 className="animate-spin" /> : <CheckCircle />}
          {isGenerating ? "Agents are analyzing..." : "Generate LaTeX Resume"}
        </button>
      </div>

      {/* RIGHT PANE: Results Preview */}
      <div className="w-1/2 bg-gray-900 text-gray-100 p-8 overflow-y-auto flex flex-col">
        {isGenerating ? (
          <div className="flex-grow flex flex-col items-center justify-center text-gray-400">
            <Loader2 className="h-12 w-12 animate-spin mb-4 text-blue-500" />
            <p className="text-lg animate-pulse">Running Multi-Agent Pipeline...</p>
            <ul className="mt-4 space-y-2 text-sm">
              <li>1. Parsing Job Requirements</li>
              <li>2. Scraping GitHub Repositories</li>
              <li>3. Selecting Top Projects</li>
              <li>4. Generating LaTeX Code</li>
            </ul>
          </div>
        ) : result ? (
          <div className="space-y-6 animate-in fade-in duration-500">
            {/* Score Card */}
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">ATS Match Analysis</h2>
                <span className={`px-4 py-1 rounded-full font-bold text-lg ${result.score > 80 ? 'bg-green-900 text-green-400' : 'bg-yellow-900 text-yellow-400'}`}>
                  {result.score}/100
                </span>
              </div>
              <p className="text-gray-300 mb-4">{result.feedback}</p>
              
              {result.missing.length > 0 && (
                <div className="flex items-start gap-2 text-sm text-red-400 bg-red-900/20 p-3 rounded-lg border border-red-900/50">
                  <AlertTriangle className="h-5 w-5 shrink-0" />
                  <p>Missing Skills: {result.missing.join(', ')}</p>
                </div>
              )}
            </div>

            {/* Code Block */}
            <div className="flex-grow flex flex-col">
              <div className="flex items-center justify-between bg-gray-800 px-4 py-2 rounded-t-lg border border-gray-700 border-b-0">
                <span className="text-sm font-mono text-gray-400">optimized_resume.tex</span>
                <button onClick={copyToClipboard} className="text-gray-400 hover:text-white transition-colors">
                  <Copy className="h-5 w-5" />
                </button>
              </div>
              <textarea 
                readOnly
                value={result.latex}
                className="w-full h-[500px] bg-gray-950 p-4 rounded-b-lg border border-gray-700 font-mono text-sm text-green-400 focus:outline-none resize-none"
              />
            </div>
          </div>
        ) : (
          <div className="flex-grow flex flex-col items-center justify-center text-gray-600">
            <FileText className="h-16 w-16 mb-4 opacity-50" />
            <p className="text-lg">Your generated LaTeX will appear here.</p>
          </div>
        )}
      </div>

      {/* CACHE MODAL POPUP */}
      {showCacheModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl shadow-2xl max-w-md w-full animate-in zoom-in duration-200">
            <h2 className="text-xl font-bold text-gray-800 mb-2 flex items-center gap-2">
              <Code className="text-gray-600" /> Existing Profile Found
            </h2>
            <p className="text-gray-600 mb-6">
              We found cached GitHub projects for <strong>{username}</strong>. Do you want to use the saved data for a faster generation, or fetch fresh data from GitHub?
            </p>
            <div className="flex gap-4">
              <button 
                onClick={() => generateResume(true)}
                className="flex-1 bg-blue-100 hover:bg-blue-200 text-blue-700 font-bold py-2 px-4 rounded-lg transition-colors"
              >
                Use Saved (Fast)
              </button>
              <button 
                onClick={() => generateResume(false)}
                className="flex-1 bg-gray-800 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded-lg transition-colors"
              >
                Fetch Fresh
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;