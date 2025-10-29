<template>
  <Layout>
    <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12 animate-fade-in">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 via-primary-600 to-blue-700 rounded-3xl mb-6 shadow-2xl shadow-primary-500/25">
            <font-awesome-icon :icon="['fas', 'magic']" class="h-10 w-10 text-white" />
          </div>
          <h1 class="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-primary-800 to-blue-800 dark:from-white dark:via-primary-200 dark:to-blue-200 mb-4">
            Create Your AI-Powered Book
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Transform your ideas into professional books with our advanced AI technology. Choose from trending niches and watch your content come to life.
          </p>
        </div>

        <!-- Progress Steps -->
        <div class="mb-12">
          <div class="flex items-center justify-between max-w-4xl mx-auto">
            <div v-for="(step, index) in steps" :key="index" class="flex-1">
              <div class="flex items-center" :class="index < steps.length - 1 ? 'mr-4' : ''">
                <div class="flex flex-col items-center flex-1">
                  <div 
                    class="w-12 h-12 rounded-full flex items-center justify-center font-bold transition-all duration-500 shadow-lg"
                    :class="currentStep > index ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-green-500/25' : currentStep === index ? 'bg-gradient-to-r from-primary-600 to-blue-700 text-white shadow-primary-500/25 ring-4 ring-primary-200 dark:ring-primary-900 animate-pulse' : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 shadow-gray-200 dark:shadow-gray-800'"
                  >
                    <font-awesome-icon v-if="currentStep > index" :icon="['fas', 'check']" class="h-6 w-6" />
                    <span v-else class="text-lg">{{ index + 1 }}</span>
                  </div>
                  <span class="text-sm mt-3 font-semibold" :class="currentStep >= index ? 'text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'">
                    {{ step }}
                  </span>
                </div>
                <div v-if="index < steps.length - 1" class="flex-1 h-1 mx-4 mt-[-20px]" :class="currentStep > index ? 'bg-gradient-to-r from-green-500 to-emerald-600' : 'bg-gray-300 dark:bg-gray-700'"></div>
              </div>
            </div>
          </div>
        </div>        <!-- Error Message -->
        <div v-if="error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-4 mb-6 border border-red-200 dark:border-red-800 animate-scale-in">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400 mt-0.5" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-300">{{ error }}</h3>
            </div>
          </div>
        </div>

        <!-- Form Card -->
        <div class="bg-white dark:bg-gray-800 shadow-2xl rounded-3xl overflow-hidden border border-gray-200 dark:border-gray-700 backdrop-blur-sm bg-white/80 dark:bg-gray-800/80 animate-slide-up">
          <form @submit.prevent="handleNext">
            <div class="p-10 sm:p-12">
              
              <!-- Step 1: Choose Domain -->
              <div v-show="currentStep === 0" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'compass']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Choose Your Book Domain
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Select the main category that best fits your book concept. We've curated 3 trending domains with custom-trained AI models for unlimited generation.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <label
                    v-for="domain in domains"
                    :key="domain.value"
                    class="group relative flex cursor-pointer rounded-2xl border-2 p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 backdrop-blur-sm"
                    :class="form.domain === domain.value ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="domain"
                      :value="domain.value"
                      v-model="form.domain"
                      class="sr-only"
                    />
                    <div class="flex flex-1 items-center">
                      <div class="flex-shrink-0 mr-4">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300" :class="form.domain === domain.value ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                          <font-awesome-icon :icon="['fas', domainIcons[domain.value] || 'book']" class="h-6 w-6" />
                        </div>
                      </div>
                      <div class="flex flex-col">
                        <span class="block text-sm font-bold mb-1" :class="form.domain === domain.value ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                          {{ domain.label }}
                        </span>
                        <span class="text-xs text-gray-500 dark:text-gray-400">
                          {{ getDomainDescription(domain.value) }}
                        </span>
                      </div>
                    </div>
                    <font-awesome-icon
                      v-if="form.domain === domain.value"
                      :icon="['fas', 'check-circle']"
                      class="h-6 w-6 text-primary-600 dark:text-primary-400 absolute top-4 right-4 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>
              </div>

              <!-- Step 2: Choose Niche -->
              <div v-show="currentStep === 1" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'bullseye']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Select Your Specific Niche
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Choose a specific niche within <strong>{{ getDomainLabel(form.domain) }}</strong>. Each niche is carefully selected based on market trends and audience demand.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <label
                    v-for="niche in availableNiches"
                    :key="niche.id"
                    class="group relative flex cursor-pointer rounded-xl border-2 p-5 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-102 backdrop-blur-sm"
                    :class="form.niche === niche.id ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="niche"
                      :value="niche.id"
                      v-model.number="form.niche"
                      class="sr-only"
                    />
                    <div class="flex flex-1 items-center">
                      <div class="flex-shrink-0 mr-4">
                        <div class="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-300" :class="form.niche === niche.id ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                          <font-awesome-icon :icon="['fas', 'star']" class="h-5 w-5" />
                        </div>
                      </div>
                      <span class="block text-sm font-semibold" :class="form.niche === niche.id ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                        {{ niche.name }}
                      </span>
                      <span class="block text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {{ niche.description || 'Curated niche workflow' }}
                      </span>
                      <span v-if="Array.isArray(niche.content_skeleton) && niche.content_skeleton.length" class="block text-xs text-primary-600 dark:text-primary-300 mt-2">
                        {{ niche.content_skeleton.length }} guided sections
                      </span>
                    </div>
                    <font-awesome-icon
                      v-if="form.niche === niche.id"
                      :icon="['fas', 'check-circle']"
                      class="h-5 w-5 text-primary-600 dark:text-primary-400 absolute top-4 right-4 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>
              </div>

              <!-- Step 3: Choose Cover Style -->
              <div v-show="currentStep === 2" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'image']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Choose Your Cover Style
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Select a cover style that matches your book's theme and audience. We'll generate professional covers based on your choice.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <label
                    v-for="style in coverStyles"
                    :key="style.id"
                    class="group relative flex cursor-pointer rounded-2xl border-2 p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 flex-col backdrop-blur-sm"
                    :class="form.cover_style === style.id ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="cover_style"
                      :value="style.id"
                      v-model.number="form.cover_style"
                      class="sr-only"
                    />
                    <div class="flex items-start mb-4">
                      <div class="w-12 h-12 rounded-xl flex items-center justify-center mr-4 transition-all duration-300" :class="form.cover_style === style.id ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                        <font-awesome-icon :icon="['fas', getCoverStyleIcon(style.style)]" class="h-6 w-6" />
                      </div>
                      <div class="flex-1">
                        <span class="text-lg font-bold mb-2 block" :class="form.cover_style === style.id ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                          {{ style.name }}
                        </span>
                        <span class="text-sm text-gray-500 dark:text-gray-400">
                          {{ style.description }}
                        </span>
                      </div>
                    </div>
                    <font-awesome-icon
                      v-if="form.cover_style === style.id"
                      :icon="['fas', 'check-circle']"
                      class="h-6 w-6 text-primary-600 dark:text-primary-400 absolute top-4 right-4 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>

                <!-- Info about cover generation -->
                <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mt-6">
                  <div class="flex">
                    <font-awesome-icon :icon="['fas', 'info-circle']" class="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-blue-800 dark:text-blue-300">Cover Generation</h3>
                      <div class="mt-2 text-sm text-blue-700 dark:text-blue-400">
                        <p>Based on your selection, we'll generate a professional cover using AI and your chosen style.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Step 4: Choose Book Length -->
              <div v-show="currentStep === 3" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'ruler']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Choose Your Book Length
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Select the ideal length for your book. Longer books provide more depth but take more time to generate.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <label
                    v-for="length in bookLengths"
                    :key="length.value"
                    class="group relative flex cursor-pointer rounded-2xl border-2 p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 backdrop-blur-sm"
                    :class="form.book_length === length.value ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="book_length"
                      :value="length.value"
                      v-model="form.book_length"
                      class="sr-only"
                    />
                    <div class="flex flex-1 items-center">
                      <div class="flex-shrink-0 mr-4">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300" :class="form.book_length === length.value ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                          <font-awesome-icon :icon="['fas', length.icon]" class="h-6 w-6" />
                        </div>
                      </div>
                      <div class="flex flex-col">
                        <span class="block text-lg font-bold mb-1" :class="form.book_length === length.value ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                          {{ length.label }}
                        </span>
                        <span class="text-sm text-gray-500 dark:text-gray-400">
                          {{ length.description }}
                        </span>
                        <span class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                          ~{{ length.pages }} pages
                        </span>
                      </div>
                    </div>
                    <font-awesome-icon
                      v-if="form.book_length === length.value"
                      :icon="['fas', 'check-circle']"
                      class="h-6 w-6 text-primary-600 dark:text-primary-400 absolute top-4 right-4 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>
              </div>

              <!-- Step 5: Review & Confirm -->
              <div v-show="currentStep === 4" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'check-square']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Review Your Book Configuration
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Please review your selections before we start generating your book. This process cannot be interrupted once started.
                </p>

                <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-6 space-y-5">
                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'compass']" class="text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Domain</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ getDomainLabel(form.domain) }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ getDomainDescription(form.domain) }}</p>
                    </div>
                  </div>

                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'bullseye']" class="text-white" />
                    </div>
                    <div class="ml-4 flex-1">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Niche</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ getNicheLabel(form.niche) }}</p>
                      <p v-if="selectedNiche?.description" class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ selectedNiche.description }}</p>
                      <div v-if="nicheSkeletonPreview.length" class="mt-3">
                        <p class="text-xs font-semibold text-primary-700 dark:text-primary-300 uppercase tracking-wide">Structured Outline</p>
                        <ul class="mt-2 space-y-1 text-xs text-gray-600 dark:text-gray-300">
                          <li v-for="(item, idx) in nicheSkeletonPreview" :key="idx" class="flex items-center">
                            <font-awesome-icon :icon="['fas', 'dot-circle']" class="h-2.5 w-2.5 text-primary-500 mr-2" />
                            <span>{{ item }}</span>
                          </li>
                        </ul>
                      </div>
                      <div v-if="selectedNiche?.prompt_template" class="mt-3">
                        <p class="text-xs font-semibold text-primary-700 dark:text-primary-300 uppercase tracking-wide">LLM Prompt</p>
                        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 truncate">{{ selectedNiche.prompt_template }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'image']" class="text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Cover Style</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ getCoverStyleLabel(form.cover_style) }}</p>
                      <p v-if="selectedCoverStyle?.description" class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ selectedCoverStyle.description }}</p>
                    </div>
                  </div>

                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'ruler']" class="text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Book Length</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ getBookLengthLabel(form.book_length) }}</p>
                      <p v-if="selectedBookLength" class="text-xs text-gray-500 dark:text-gray-400 mt-1">~{{ selectedBookLength.pages }} pages · {{ selectedBookLength.description }}</p>
                    </div>
                  </div>
                </div>

                <!-- What happens next -->
                <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
                  <div class="flex">
                    <font-awesome-icon :icon="['fas', 'clock']" class="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-300">What Happens Next?</h3>
                      <div class="mt-2 text-sm text-yellow-700 dark:text-yellow-400">
                        <ol class="list-decimal list-inside space-y-1">
                          <li>AI generates your book content based on selected style</li>
                          <li>System creates a professional cover based on your cover style selection</li>
                          <li>Your book is automatically assembled and ready to download</li>
                        </ol>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- Action Buttons -->
            <div class="bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900/50 dark:to-blue-900/50 px-10 py-8 sm:px-12 flex items-center justify-between border-t border-gray-200 dark:border-gray-700">
              <button
                v-if="currentStep > 0"
                type="button"
                @click="handleBack"
                class="inline-flex items-center px-8 py-4 border-2 border-gray-300 dark:border-gray-600 text-sm font-semibold rounded-xl text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 active:scale-95"
              >
                <font-awesome-icon :icon="['fas', 'arrow-left']" class="mr-3 h-4 w-4" />
                Back
              </button>
              <div v-else></div>

              <button
                type="submit"
                :disabled="loading || !isStepValid"
                class="inline-flex items-center px-10 py-4 border border-transparent text-sm font-bold rounded-xl text-white bg-gradient-to-r from-primary-600 via-primary-700 to-blue-700 hover:from-primary-700 hover:via-primary-800 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 active:scale-95 transition-all duration-300 shadow-xl shadow-primary-500/25 hover:shadow-2xl hover:shadow-primary-500/40"
              >
                <span v-if="!loading">
                  <font-awesome-icon v-if="currentStep < steps.length - 1" :icon="['fas', 'arrow-right']" class="mr-3 h-4 w-4" />
                  <font-awesome-icon v-else :icon="['fas', 'magic']" class="mr-3 h-4 w-4" />
                  {{ currentStep < steps.length - 1 ? 'Continue' : 'Generate My Book' }}
                </span>
                <span v-else class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-3 h-4 w-4" />
                  Creating...
                </span>
              </button>
            </div>
          </form>
        </div>

        <!-- Trending Niches Info -->
        <div class="mt-12 bg-gradient-to-r from-primary-50 via-blue-50 to-indigo-50 dark:from-primary-900/20 dark:via-blue-900/20 dark:to-indigo-900/20 rounded-3xl p-8 shadow-xl border border-primary-200 dark:border-primary-800 backdrop-blur-sm">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <div class="w-10 h-10 bg-gradient-to-r from-primary-600 to-blue-700 rounded-xl flex items-center justify-center mr-4 shadow-lg">
              <font-awesome-icon :icon="['fas', 'chart-line']" class="h-5 w-5 text-white" />
            </div>
            Why These Niches?
          </h3>
          <p class="text-lg text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">
            Our 9 sub-niches across 3 trending domains are carefully curated and powered by custom-trained AI models for unlimited, instant book generation.
          </p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="flex items-start">
              <div class="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'search']" class="h-6 w-6 text-white" />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Market Research</h4>
                <p class="text-gray-600 dark:text-gray-400">2025 Google Trends analysis and audience demand data drive our selections.</p>
              </div>
            </div>
            <div class="flex items-start">
              <div class="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'users']" class="h-6 w-6 text-white" />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Proven Demand</h4>
                <p class="text-gray-600 dark:text-gray-400">Active communities and high search volumes ensure market viability.</p>
              </div>
            </div>
            <div class="flex items-start">
              <div class="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'dollar-sign']" class="h-6 w-6 text-white" />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Monetization Potential</h4>
                <p class="text-gray-600 dark:text-gray-400">Strong buyer intent and evergreen topics maximize earning potential.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import Layout from '../../components/Layout.vue';
import { api } from '../../services/api';

const router = useRouter();
const authStore = useAuthStore();

const currentStep = ref(0);
const loading = ref(false);
const error = ref('');

const steps = ['Domain', 'Niche', 'Cover Style', 'Book Length', 'Confirm'];

const form = ref({
  domain: '' as string,
  niche: null as number | null,
  cover_style: null as number | null,
  book_length: 'standard' as 'short' | 'standard' | 'long',
});

const domains = ref<Array<{value: string, label: string, description?: string, icon?: string}>>([
  { value: 'ai_automation', label: 'AI & Automation', description: 'AI tools, automation strategies, and intelligent systems' },
  { value: 'parenting', label: 'Parenting: Pre-school Speech & Learning', description: 'Early childhood development, speech therapy, and preschool learning' },
  { value: 'ecommerce', label: 'E-commerce & Digital Products', description: 'Online business, digital products, and e-commerce strategies' }
]);

const domainIcons: Record<string, string> = {
  'ai_automation': 'robot',
  'parenting': 'child',
  'ecommerce': 'shopping-cart'
};

const availableNiches = ref<any[]>([]);
const coverStyles = ref<any[]>([]);
const bookLengths = ref([
  { value: 'short', label: 'Short Book', description: 'Focused primer ideal for quick wins and lead magnets', pages: '20-25', icon: 'file-alt' },
  { value: 'standard', label: 'Standard Book', description: 'Balanced depth with detailed chapters and case studies', pages: '35-45', icon: 'book' },
  { value: 'long', label: 'Long Book', description: 'Comprehensive playbook with advanced frameworks and examples', pages: '50-70', icon: 'book-open' }
]);

const selectedNiche = computed(() => {
  if (form.value.niche == null) {
    return null;
  }
  return availableNiches.value.find((n: any) => n.id === form.value.niche) || null;
});

const selectedCoverStyle = computed(() => {
  if (form.value.cover_style == null) {
    return null;
  }
  return coverStyles.value.find((style: any) => style.id === form.value.cover_style) || null;
});

// Watch for domain changes and reload niches
watch(
  () => form.value.domain,
  async (newDomain, oldDomain) => {
    if (!newDomain || newDomain === oldDomain) {
      return;
    }

    console.log(`[Domain Change] Loading niches for domain: ${newDomain}`);
    form.value.niche = null;
    availableNiches.value = [];

    try {
      const response = await api.getNiches(newDomain);
      availableNiches.value = response.data || [];
      console.log(`[Domain Change] Loaded ${availableNiches.value.length} niches for ${newDomain}`);
    } catch (err) {
      console.error('[Domain Change] Failed to load niches:', err);
      error.value = 'Failed to load niches for selected domain';
    }
  },
  { immediate: false }
);

const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 0:
      return form.value.domain.trim().length > 0;
    case 1:
      return form.value.niche != null;
    case 2:
      return form.value.cover_style != null;
    case 3:
      return !!form.value.book_length;
    case 4:
      return true;
    default:
      return false;
  }
});

onMounted(async () => {
  // Check authentication
  if (!authStore.isAuthenticated) {
    router.push('/auth/signin');
    return;
  }

  try {
    // Load domains from API and convert to expected format
    const domainsResponse = await api.getDomains();
    const apiDomains = domainsResponse.data || [];
    domains.value = apiDomains.map((domain: any) => ({
      value: domain.slug, // Use slug as value
      label: domain.name,
      description: domain.description,
      icon: domain.icon
    }));

    // Load cover styles
    const coverStylesResponse = await api.getCoverStyles();
    coverStyles.value = coverStylesResponse.data || [];

    console.log('[Initial Load] Loaded domains:', domains.value);
    console.log('[Initial Load] Loaded cover styles:', coverStyles.value);
    console.log('[Initial Load] Niches will be loaded when domain is selected');
  } catch (err) {
    error.value = 'Failed to load book configuration';
    console.error('[Initial Load] Failed to load configuration:', err);
  }
});

const getDomainLabel = (value: string) => {
  const domain = domains.value.find(d => d.value === value);
  return domain ? domain.label : value;
};

const getNicheLabel = (value: number | null) => {
  if (value == null) {
    return 'Select a niche';
  }
  const niche = availableNiches.value.find((n: any) => n.id === value);
  return niche ? niche.name : 'Custom niche';
};

const getDomainDescription = (value: string) => {
  const domain = domains.value.find(d => d.value === value);
  return domain ? domain.description : 'Trending niche content';
};

const getCoverStyleIcon = (style: string) => {
  const iconMap: Record<string, string> = {
    'minimalist': 'square',
    'futuristic': 'rocket',
    'playful': 'smile',
    'elegant': 'crown',
    'corporate': 'building',
    'artistic': 'palette'
  };
  return iconMap[style] || 'image';
};

const getBookLengthLabel = (value: string) => {
  const length = bookLengths.value.find(l => l.value === value);
  return length ? length.label : value;
};

const getCoverStyleLabel = (value: number | null) => {
  if (value == null) {
    return 'Select a cover style';
  }
  const style = coverStyles.value.find((s: any) => s.id === value);
  return style ? style.name : 'Custom cover style';
};

const formatSkeletonItem = (item: any, index: number) => {
  if (!item) {
    return `Section ${index + 1}`;
  }
  if (typeof item === 'string') {
    return item;
  }
  return item.title || item.name || item.label || item.stage || `Section ${index + 1}`;
};

const nicheSkeletonPreview = computed(() => {
  const skeleton = selectedNiche.value?.content_skeleton;
  if (!Array.isArray(skeleton)) {
    return [] as string[];
  }
  return skeleton
    .map((item: any, index: number) => formatSkeletonItem(item, index))
    .filter((text: string) => Boolean(text))
    .slice(0, 6);
});

const selectedBookLength = computed(() => {
  return bookLengths.value.find((length: any) => length.value === form.value.book_length) || null;
});

const handleNext = async () => {
  error.value = '';
  
  if (currentStep.value < steps.length - 1) {
    currentStep.value++;
  } else {
    // Submit the form
    await handleSubmit();
  }
};

const handleBack = () => {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
};

const handleSubmit = async () => {
  try {
    loading.value = true;
    error.value = '';

    if (form.value.niche == null || form.value.cover_style == null) {
      throw new Error('Please select a niche and cover style before continuing');
    }

    const payload = {
      domain: form.value.domain,
      niche: form.value.niche,
      cover_style: form.value.cover_style,
      book_length: form.value.book_length,
    };

    console.log('Submitting book creation with data:', payload);
    const response = await api.createGuidedBook(payload);
    const book = response.data;

    // Validate response has book ID before redirect
    if (!book || !book.id) {
      throw new Error('Server did not return book data');
    }

    // Redirect to book details page to monitor progress
    router.push(`/profile/books/${book.id}`);
  } catch (err: any) {
    console.error('Create book error details:', err.response?.data);
    console.error('Create book error status:', err.response?.status);
    console.error('Create book error headers:', err.response?.headers);
    
    let errorMessage = 'Failed to create book';
    if (err.response?.data) {
      if (typeof err.response.data === 'string') {
        errorMessage = err.response.data;
      } else if (err.response.data.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response.data.error) {
        errorMessage = err.response.data.error;
      } else if (typeof err.response.data === 'object') {
        // Handle validation errors
        const errors = [];
        for (const [field, fieldErrors] of Object.entries(err.response.data)) {
          if (Array.isArray(fieldErrors)) {
            errors.push(`${field}: ${fieldErrors.join(', ')}`);
          } else {
            errors.push(`${field}: ${fieldErrors}`);
          }
        }
        errorMessage = errors.join('; ');
      }
    } else if (err.message) {
      errorMessage = err.message;
    }
    
    error.value = errorMessage;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.8s ease-out;
}

.animate-scale-in {
  animation: scale-in 0.4s ease-out;
}

.animate-pulse-glow {
  animation: pulse-glow 2s infinite;
}

/* Hover effects */
.hover\:scale-102:hover {
  transform: scale(1.02);
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Glass morphism effect */
.glass {
  backdrop-filter: blur(16px) saturate(180%);
  background-color: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(209, 213, 219, 0.3);
}

/* Custom scrollbar for the component */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a67d8, #6b46c1);
}
</style>
