"use client"

import React, { useState, useEffect } from "react"
import { 
  FileText, 
  Globe, 
  Database, 
  HelpCircle, 
  DollarSign, 
  Plus, 
  Edit, 
  Zap, 
  Clock,
  CheckCircle,
  AlertCircle,
  X
} from "lucide-react"

interface KnowledgeDoc {
  id: number
  slug: string
  title: string
  type: "kb_json" | "blog_md" | "pricing_json" | "faq_md" | "external_url"
  lang: string
  enabled: boolean
  priority: number
  content?: string
  source_path?: string
  url?: string
  checksum?: string
  embedded_at?: string | null
  updated_at: string
}

interface KnowledgeDocForm {
  slug: string
  title: string
  type: "kb_json" | "blog_md" | "pricing_json" | "faq_md" | "external_url"
  lang: string
  enabled: boolean
  priority: number
  content: string
  source_path: string
  url: string
}

const TYPE_LABELS = {
  kb_json: "KB JSON",
  blog_md: "Blog Markdown", 
  pricing_json: "Pricing JSON",
  faq_md: "FAQ Markdown",
  external_url: "External URL"
}

const TYPE_ICONS = {
  kb_json: Database,
  blog_md: FileText,
  pricing_json: DollarSign,
  faq_md: HelpCircle,
  external_url: Globe
}

const LANG_OPTIONS = [
  { value: "en", label: "English" },
  { value: "nl", label: "Dutch" },
  { value: "fr", label: "French" },
  { value: "es", label: "Spanish" },
  { value: "pt", label: "Portuguese" },
  { value: "multi", label: "Multi-language" }
]

export default function AssistantKBPanel() {
  const [docs, setDocs] = useState<KnowledgeDoc[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editDoc, setEditDoc] = useState<KnowledgeDoc | null>(null)
  const [formData, setFormData] = useState<KnowledgeDocForm>({
    slug: "",
    title: "",
    type: "kb_json",
    lang: "en",
    enabled: true,
    priority: 0,
    content: "",
    source_path: "",
    url: ""
  })
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [isEmbedding, setIsEmbedding] = useState<number | null>(null)

  const fetchDocs = async () => {
    try {
      const response = await fetch("/api/assistant/kb")
      if (!response.ok) throw new Error("Failed to fetch KB documents")
      const data = await response.json()
      setDocs(data.items || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load KB documents")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDocs()
  }, [])

  const resetForm = () => {
    setFormData({
      slug: "",
      title: "",
      type: "kb_json",
      lang: "en", 
      enabled: true,
      priority: 0,
      content: "",
      source_path: "",
      url: ""
    })
    setEditDoc(null)
  }

  const handleCreate = () => {
    resetForm()
    setIsDialogOpen(true)
  }

  const handleEdit = (doc: KnowledgeDoc) => {
    setFormData({
      slug: doc.slug,
      title: doc.title,
      type: doc.type,
      lang: doc.lang,
      enabled: doc.enabled,
      priority: doc.priority,
      content: doc.content || "",
      source_path: doc.source_path || "",
      url: doc.url || ""
    })
    setEditDoc(doc)
    setIsDialogOpen(true)
  }

  const handleSave = async () => {
    try {
      const url = "/api/assistant/kb"
      const method = editDoc ? "PATCH" : "POST"
      const body = editDoc ? { ...formData, id: editDoc.id } : formData

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Failed to save document")
      }

      await fetchDocs()
      setIsDialogOpen(false)
      resetForm()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save document")
    }
  }

  const handleEmbed = async (doc: KnowledgeDoc) => {
    setIsEmbedding(doc.id)
    try {
      const response = await fetch("/api/assistant/kb/embed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: doc.id })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Failed to embed document")
      }

      await fetchDocs()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to embed document")
    } finally {
      setIsEmbedding(null)
    }
  }

  const getSourceInfo = (doc: KnowledgeDoc) => {
    if (doc.content) return { type: "content", value: `${doc.content.length} characters` }
    if (doc.source_path) return { type: "path", value: doc.source_path }
    if (doc.url) return { type: "url", value: doc.url }
    return { type: "empty", value: "No source" }
  }

  const formatDateTime = (dateStr: string | null) => {
    if (!dateStr) return "Never"
    return new Date(dateStr).toLocaleString()
  }

  if (loading) return <div className="p-4">Loading KB documents...</div>

  return (
    <div className="bg-white rounded-lg shadow border">
      <div className="border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <Database className="h-5 w-5" />
            Knowledge Base Documents
          </h3>
          <button
            onClick={handleCreate}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Document
          </button>
        </div>
      </div>
      
      <div className="p-6">
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-700">
            {error}
          </div>
        )}

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Document</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Language</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Embedded</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {docs.map((doc) => {
                const TypeIcon = TYPE_ICONS[doc.type]
                const sourceInfo = getSourceInfo(doc)
                
                return (
                  <tr key={doc.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="font-medium text-gray-900">{doc.title}</div>
                        <div className="text-sm text-gray-500">{doc.slug}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <TypeIcon className="h-4 w-4" />
                        <span className="text-sm">{TYPE_LABELS[doc.type]}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        {doc.lang.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">
                        <div className="capitalize">{sourceInfo.type}</div>
                        <div className="text-gray-500 truncate max-w-32">{sourceInfo.value}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        {doc.enabled ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Enabled
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            <AlertCircle className="h-3 w-3 mr-1" />
                            Disabled
                          </span>
                        )}
                        <span className="text-xs text-gray-500">P{doc.priority}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">
                        {doc.embedded_at ? (
                          <div className="text-green-600">
                            <Clock className="h-3 w-3 inline mr-1" />
                            {formatDateTime(doc.embedded_at)}
                          </div>
                        ) : (
                          <span className="text-gray-400">Not embedded</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleEdit(doc)}
                          className="inline-flex items-center px-2.5 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                          <Edit className="h-3 w-3" />
                        </button>
                        <button
                          onClick={() => handleEmbed(doc)}
                          disabled={isEmbedding === doc.id}
                          className="inline-flex items-center px-2.5 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                        >
                          <Zap className={`h-3 w-3 ${isEmbedding === doc.id ? 'animate-pulse' : ''}`} />
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {docs.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No knowledge base documents found. Create your first document to get started.
          </div>
        )}

        {/* Modal Dialog */}
        {isDialogOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="border-b border-gray-200 px-6 py-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {editDoc ? "Edit Knowledge Document" : "Create Knowledge Document"}
                  </h3>
                  <button
                    onClick={() => setIsDialogOpen(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="h-6 w-6" />
                  </button>
                </div>
              </div>
              
              <div className="p-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="slug" className="block text-sm font-medium text-gray-700 mb-1">Slug</label>
                    <input
                      id="slug"
                      type="text"
                      value={formData.slug}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData(prev => ({ ...prev, slug: e.target.value }))}
                      placeholder="unique-identifier"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                    <input
                      id="title"
                      type="text"
                      value={formData.title}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                      placeholder="Document Title"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <select
                      id="type"
                      value={formData.type}
                      onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFormData(prev => ({ ...prev, type: e.target.value as any }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {Object.entries(TYPE_LABELS).map(([value, label]) => (
                        <option key={value} value={value}>{label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="lang" className="block text-sm font-medium text-gray-700 mb-1">Language</label>
                    <select
                      id="lang"
                      value={formData.lang}
                      onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFormData(prev => ({ ...prev, lang: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {LANG_OPTIONS.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                    <input
                      id="priority"
                      type="number"
                      value={formData.priority}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData(prev => ({ ...prev, priority: parseInt(e.target.value) || 0 }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <input
                    id="enabled"
                    type="checkbox"
                    checked={formData.enabled}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData(prev => ({ ...prev, enabled: e.target.checked }))}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="enabled" className="text-sm font-medium text-gray-700">Enabled</label>
                </div>

                <div className="space-y-4">
                  <label className="block text-sm font-medium text-gray-700">Content Source</label>
                  
                  <div>
                    <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">Direct Content</label>
                    <textarea
                      id="content"
                      value={formData.content}
                      onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                      rows={6}
                      placeholder="Paste your content here..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="source_path" className="block text-sm font-medium text-gray-700 mb-1">Source File Path</label>
                    <input
                      id="source_path"
                      type="text"
                      value={formData.source_path}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData(prev => ({ ...prev, source_path: e.target.value }))}
                      placeholder="/path/to/file.md"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-1">External URL</label>
                    <input
                      id="url"
                      type="text"
                      value={formData.url}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData(prev => ({ ...prev, url: e.target.value }))}
                      placeholder="https://example.com/document"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-2 pt-4">
                  <button
                    onClick={() => setIsDialogOpen(false)}
                    className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    {editDoc ? "Update" : "Create"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}