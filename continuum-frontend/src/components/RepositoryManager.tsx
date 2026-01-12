import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  GitBranch,
  Plus,
  Trash2,
  ExternalLink,
  AlertCircle,
  CheckCircle,
  Loader2,
  X
} from 'lucide-react';
import { repositoriesApi } from '../api/repositories';
import type { Repository, GitProvider } from '../api/repositories';

interface RepositoryManagerProps {
  projectId: number;
  projectName?: string;
}

const PROVIDER_ICONS: Record<GitProvider, string> = {
  github: '🐙',
  gitlab: '🦊',
  bitbucket: '🪣',
};

const PROVIDER_COLORS: Record<GitProvider, string> = {
  github: 'bg-gray-800 border-gray-700',
  gitlab: 'bg-orange-900/30 border-orange-700/50',
  bitbucket: 'bg-blue-900/30 border-blue-700/50',
};

export default function RepositoryManager({ projectId, projectName }: RepositoryManagerProps) {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState({
    repository_url: '',
    repository_name: '',
    provider: 'github' as GitProvider,
    webhook_secret: '',
  });

  const fetchRepositories = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await repositoriesApi.getByProject(projectId);
      setRepositories(data);
    } catch (err) {
      setError('Failed to load repositories');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRepositories();
  }, [projectId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const newRepo = await repositoriesApi.link(projectId, {
        project_id: projectId,
        repository_url: formData.repository_url,
        repository_name: formData.repository_name,
        provider: formData.provider,
        webhook_secret: formData.webhook_secret || undefined,
      });

      setRepositories(prev => [...prev, newRepo]);
      setShowAddForm(false);
      setFormData({
        repository_url: '',
        repository_name: '',
        provider: 'github',
        webhook_secret: '',
      });
      setSuccessMessage('Repository linked successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error
        ? err.message
        : (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to link repository';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUnlink = async (repoId: number, repoName: string) => {
    if (!confirm(`Are you sure you want to unlink "${repoName}"?`)) return;

    try {
      await repositoriesApi.unlink(repoId);
      setRepositories(prev => prev.filter(r => r.id !== repoId));
      setSuccessMessage('Repository unlinked successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError('Failed to unlink repository');
      console.error(err);
    }
  };

  const extractRepoName = (url: string): string => {
    try {
      const match = url.match(/(?:github|gitlab|bitbucket)[.com|.org]+\/(.+?)(?:\.git)?$/i);
      return match ? match[1] : url;
    } catch {
      return url;
    }
  };

  const handleUrlChange = (url: string) => {
    setFormData(prev => ({
      ...prev,
      repository_url: url,
      repository_name: prev.repository_name || extractRepoName(url),
    }));

    // Auto-detect provider
    if (url.includes('github')) {
      setFormData(prev => ({ ...prev, provider: 'github' }));
    } else if (url.includes('gitlab')) {
      setFormData(prev => ({ ...prev, provider: 'gitlab' }));
    } else if (url.includes('bitbucket')) {
      setFormData(prev => ({ ...prev, provider: 'bitbucket' }));
    }
  };

  return (
    <div className="bg-slate-900/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-500/20 rounded-lg">
            <GitBranch className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Repository Mapping</h3>
            <p className="text-sm text-slate-400">
              Link Git repositories for webhook integration
              {projectName && <span className="text-slate-500"> • {projectName}</span>}
            </p>
          </div>
        </div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-500
                     text-white rounded-lg transition-colors text-sm font-medium"
        >
          <Plus className="w-4 h-4" />
          Link Repository
        </motion.button>
      </div>

      {/* Success Message */}
      <AnimatePresence>
        {successMessage && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-4 p-3 bg-green-500/20 border border-green-500/30 rounded-lg
                       flex items-center gap-2 text-green-400"
          >
            <CheckCircle className="w-4 h-4" />
            <span className="text-sm">{successMessage}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg
                       flex items-center justify-between text-red-400"
          >
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
            </div>
            <button onClick={() => setError(null)}>
              <X className="w-4 h-4 hover:text-red-300" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Add Repository Form */}
      <AnimatePresence>
        {showAddForm && (
          <motion.form
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            onSubmit={handleSubmit}
            className="mb-6 p-4 bg-slate-800/50 border border-slate-700/50 rounded-xl overflow-hidden"
          >
            <div className="grid gap-4">
              {/* Repository URL */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">
                  Repository URL *
                </label>
                <input
                  type="url"
                  required
                  placeholder="https://github.com/org/repo"
                  value={formData.repository_url}
                  onChange={(e) => handleUrlChange(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-900/50 border border-slate-600 rounded-lg
                           text-white placeholder-slate-500 focus:outline-none focus:border-purple-500
                           transition-colors"
                />
              </div>

              {/* Repository Name */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">
                  Repository Name *
                </label>
                <input
                  type="text"
                  required
                  placeholder="org/repo"
                  value={formData.repository_name}
                  onChange={(e) => setFormData(prev => ({ ...prev, repository_name: e.target.value }))}
                  className="w-full px-3 py-2 bg-slate-900/50 border border-slate-600 rounded-lg
                           text-white placeholder-slate-500 focus:outline-none focus:border-purple-500
                           transition-colors"
                />
              </div>

              {/* Provider */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">
                  Provider *
                </label>
                <div className="flex gap-2">
                  {(['github', 'gitlab', 'bitbucket'] as GitProvider[]).map((provider) => (
                    <button
                      key={provider}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, provider }))}
                      className={`flex-1 py-2 px-3 rounded-lg border transition-all text-sm font-medium
                        ${formData.provider === provider
                          ? `${PROVIDER_COLORS[provider]} text-white ring-2 ring-purple-500/50`
                          : 'bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-600'
                        }`}
                    >
                      <span className="mr-1.5">{PROVIDER_ICONS[provider]}</span>
                      {provider.charAt(0).toUpperCase() + provider.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Webhook Secret (Optional) */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">
                  Webhook Secret <span className="text-slate-500">(optional)</span>
                </label>
                <input
                  type="password"
                  placeholder="Optional webhook secret for verification"
                  value={formData.webhook_secret}
                  onChange={(e) => setFormData(prev => ({ ...prev, webhook_secret: e.target.value }))}
                  className="w-full px-3 py-2 bg-slate-900/50 border border-slate-600 rounded-lg
                           text-white placeholder-slate-500 focus:outline-none focus:border-purple-500
                           transition-colors"
                />
              </div>

              {/* Form Actions */}
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="flex-1 py-2 px-4 bg-slate-700 hover:bg-slate-600 text-white
                           rounded-lg transition-colors text-sm font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 py-2 px-4 bg-purple-600 hover:bg-purple-500 text-white
                           rounded-lg transition-colors text-sm font-medium disabled:opacity-50
                           disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Linking...
                    </>
                  ) : (
                    'Link Repository'
                  )}
                </button>
              </div>
            </div>
          </motion.form>
        )}
      </AnimatePresence>

      {/* Repository List */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 text-purple-400 animate-spin" />
        </div>
      ) : repositories.length === 0 ? (
        <div className="text-center py-12">
          <GitBranch className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-slate-400 mb-1">No repositories linked</p>
          <p className="text-sm text-slate-500">
            Link a repository to enable webhook integration
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {repositories.map((repo) => (
            <motion.div
              key={repo.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-4 rounded-xl border ${PROVIDER_COLORS[repo.provider]}
                         flex items-center justify-between`}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl">{PROVIDER_ICONS[repo.provider]}</span>
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <h4 className="font-medium text-white truncate">
                      {repo.repository_name}
                    </h4>
                    {repo.is_active && (
                      <span className="px-1.5 py-0.5 bg-green-500/20 text-green-400
                                     text-xs rounded-full">
                        Active
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-slate-400 truncate">
                    {repo.repository_url}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2 ml-4">
                <a
                  href={repo.repository_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 text-slate-400 hover:text-white hover:bg-slate-700/50
                           rounded-lg transition-colors"
                  title="Open repository"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
                <button
                  onClick={() => handleUnlink(repo.id, repo.repository_name)}
                  className="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10
                           rounded-lg transition-colors"
                  title="Unlink repository"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Webhook Info */}
      {repositories.length > 0 && (
        <div className="mt-6 p-4 bg-slate-800/30 border border-slate-700/30 rounded-xl">
          <h4 className="text-sm font-medium text-slate-300 mb-2">
            Webhook Configuration
          </h4>
          <p className="text-xs text-slate-500 mb-2">
            Configure your repository webhooks to point to these endpoints:
          </p>
          <div className="space-y-1 text-xs font-mono text-slate-400">
            <p>GitHub: <code className="text-purple-400">/api/v1/webhooks/github</code></p>
            <p>GitLab: <code className="text-purple-400">/api/v1/webhooks/gitlab</code></p>
            <p>Bitbucket: <code className="text-purple-400">/api/v1/webhooks/bitbucket</code></p>
          </div>
        </div>
      )}
    </div>
  );
}
