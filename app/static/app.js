document.addEventListener('DOMContentLoaded', () => {
    // API base URL
    const API_URL = '/api/v1';

    // State Variables
    let currentFile = null;
    let preloadedPrompts = [];
    let mediaRecorder = null;
    let audioChunks = [];
    let recordTimerInterval = null;
    let recordStartTime = null;
    let currentTtsAudio = null;
    let recordedDuration = 0;
    let currentAudioDuration = 0;

    // DOM Elements
    const recordBtn = document.getElementById('record-btn');
    const recordStatus = document.getElementById('record-status');
    const recordTimer = document.getElementById('record-timer');
    const waveContainer = document.getElementById('wave-container');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileDetails = document.getElementById('file-details');
    const fileNameDisplay = document.getElementById('file-name');
    const clearFileBtn = document.getElementById('clear-file');
    const samplesList = document.getElementById('samples-list');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const runPipelineBtn = document.getElementById('run-pipeline-btn');
    const ttsBtn = document.getElementById('tts-btn');
    const ttsVoiceSelect = document.getElementById('tts-voice-select');

    // Pipeline Step Elements
    const stepAudio = document.getElementById('step-audio');
    const stepAudioDetails = document.getElementById('step-audio-details');
    const audioMetaInfo = document.getElementById('audio-meta-info');
    const stepAudioBadge = document.getElementById('audio-type-badge');
    
    const stepAsr = document.getElementById('step-asr');
    const stepAsrDetails = document.getElementById('step-asr-details');
    
    const stepLlm = document.getElementById('step-llm');
    const stepLlmDetails = document.getElementById('step-llm-details');
    
    const stepTool = document.getElementById('step-tool');
    const stepToolDetails = document.getElementById('step-tool-details');
    
    const stepResponse = document.getElementById('step-response');
    const stepResponseDetails = document.getElementById('step-response-details');

    const audioPlayerContainer = document.getElementById('audio-player-container');
    const audioPlayer = document.getElementById('audio-player');

    // Initialize Toast Container
    const toastContainer = document.getElementById('toast-container');

    // 1. Toast Alert Helper
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = 'fa-circle-info';
        if (type === 'success') icon = 'fa-circle-check';
        if (type === 'error') icon = 'fa-circle-exclamation';
        
        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // 2. Load Preloaded Samples
    async function loadSamples() {
        try {
            const response = await fetch(`${API_URL}/chatbot/prompts`);
            if (!response.ok) throw new Error('Không thể tải các ca kiểm thử mẫu');
            
            preloadedPrompts = await response.json();
            renderSamples('all');
        } catch (error) {
            console.error(error);
            samplesList.innerHTML = `<div class="placeholder-text" style="color: var(--danger)"><i class="fa-solid fa-triangle-exclamation"></i> Lỗi khi nạp danh sách prompts mẫu.</div>`;
            showToast('Lỗi khi nạp dữ liệu mẫu thử nghiệm!', 'error');
        }
    }

    function renderSamples(filter) {
        samplesList.innerHTML = '';
        
        const filtered = preloadedPrompts.filter(p => {
            if (filter === 'all') return true;
            return p.domain === filter;
        });

        if (filtered.length === 0) {
            samplesList.innerHTML = '<div class="placeholder-text">Không có mẫu nào.</div>';
            return;
        }

        filtered.forEach(p => {
            const item = document.createElement('div');
            item.className = 'sample-item';
            item.dataset.id = p.id;
            item.dataset.file = `${p.id}_${p.category}.mp3`; // Maps to standard filename
            
            const tagClass = p.domain === 'ride' ? 'tag-ride' : 'tag-food';
            const tagText = p.domain === 'ride' ? 'Xe' : 'Ăn';

            item.innerHTML = `
                <span class="sample-tag ${tagClass}">${tagText}</span>
                <div class="sample-text">${p.text}</div>
            `;

            item.addEventListener('click', () => selectSample(p, item));
            samplesList.appendChild(item);
        });
    }

    async function selectSample(sample, element) {
        // Remove selection from others
        document.querySelectorAll('.sample-item').forEach(el => el.classList.remove('selected'));
        element.classList.add('selected');

        // Reset file upload state
        clearFileInput();
        
        const fileName = `${sample.id}_${sample.category}.mp3`;
        fileNameDisplay.textContent = `Mẫu: ${sample.id} (${sample.category})`;
        fileDetails.classList.remove('hidden');
        dropZone.classList.add('hidden');

        // Update Step 1 Status
        stepAudioBadge.textContent = 'Mẫu có sẵn';
        stepAudioBadge.className = 'step-badge badge-whisper';
        audioMetaInfo.innerHTML = `
            <p style="margin-bottom: 8px;"><strong>Đã chọn mẫu:</strong> ${sample.id} - ${sample.category}</p>
            <p style="margin-bottom: 8px; color: var(--text-secondary); font-style: italic;">"${sample.text}"</p>
        `;

        // Fetch the audio file from static server
        try {
            showToast(`Đang tải file âm thanh ${sample.id}...`);
            const audioUrl = `/static/samples/${fileName}`;
            const response = await fetch(audioUrl);
            if (!response.ok) throw new Error('Không thể tải file âm thanh mẫu từ server');
            
            const blob = await response.blob();
            currentFile = new File([blob], fileName, { type: 'audio/mpeg' });
            
            // Set up player
            recordedDuration = 0; // Reset for sample files
            audioPlayer.src = audioUrl;
            audioPlayerContainer.classList.remove('hidden');
            
            runPipelineBtn.removeAttribute('disabled');
            showToast('Nạp tệp âm thanh mẫu thành công!', 'success');
            
            // Highlight step 1 as success
            resetPipelineVisuals();
            stepAudio.className = 'pipeline-step success';
        } catch (err) {
            console.error(err);
            showToast('Tệp âm thanh mẫu chưa được cấu hình trên hệ thống!', 'error');
            audioMetaInfo.innerHTML += `<p style="color: var(--danger); font-size: 12px; margin-top: 4px;"><i class="fa-solid fa-circle-exclamation"></i> Lỗi: Không thể chạy trình phát âm thanh do thiếu file sample trên server.</p>`;
            // We still allow running since backend can fallback transcribe, but player is disabled
            currentFile = null;
            runPipelineBtn.setAttribute('disabled', 'true');
        }
    }

    // 3. Audio Recording
    recordBtn.addEventListener('click', async () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            stopRecording();
        } else {
            startRecording();
        }
    });

    async function startRecording() {
        audioChunks = [];
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Handle different codecs depending on browser
            let options = { mimeType: 'audio/webm' };
            if (MediaRecorder.isTypeSupported('audio/mpeg')) {
                options = { mimeType: 'audio/mpeg' };
            } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                options = { mimeType: 'audio/mp4' };
            } else if (MediaRecorder.isTypeSupported('audio/ogg')) {
                options = { mimeType: 'audio/ogg' };
            }

            mediaRecorder = new MediaRecorder(stream, options);
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: options.mimeType });
                const extension = options.mimeType.includes('mpeg') ? 'mp3' : 
                                  options.mimeType.includes('ogg') ? 'ogg' : 'wav';
                                  
                const recordedFileName = `recorded_voice_${Date.now()}.${extension}`;
                currentFile = new File([audioBlob], recordedFileName, { type: audioBlob.type });
                
                // Track recording duration
                recordedDuration = (Date.now() - recordStartTime) / 1000;
                
                // Set up player
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayer.src = audioUrl;
                audioPlayerContainer.classList.remove('hidden');
                
                stepAudioBadge.textContent = 'Ghi âm trực tiếp';
                stepAudioBadge.className = 'step-badge badge-db';
                audioMetaInfo.innerHTML = `
                    <p style="margin-bottom: 8px;"><strong>Giọng nói ghi trực tiếp:</strong> ${recordedFileName}</p>
                    <p style="margin-bottom: 8px; color: var(--text-muted); font-size: 11px;">Dung lượng: ${(audioBlob.size / 1024).toFixed(1)} KB</p>
                `;
                
                // Highlight Step 1 as success
                resetPipelineVisuals();
                stepAudio.className = 'pipeline-step success';

                fileNameDisplay.textContent = 'Đã ghi âm giọng nói';
                fileDetails.classList.remove('hidden');
                dropZone.classList.add('hidden');
                runPipelineBtn.removeAttribute('disabled');
                
                showToast('Ghi âm thành công!', 'success');
                
                // Stop microphone tracks
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.start();
            recordStartTime = Date.now();
            recordTimerInterval = setInterval(updateRecordTimer, 1000);
            
            recordBtn.classList.add('recording');
            recordStatus.textContent = 'Đang ghi âm...';
            recordTimer.classList.remove('hidden');
            waveContainer.classList.remove('hidden');
            
            // Deselect samples
            document.querySelectorAll('.sample-item').forEach(el => el.classList.remove('selected'));
            
        } catch (err) {
            console.error('Không thể truy cập microphone:', err);
            showToast('Không thể truy cập microphone của bạn!', 'error');
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            clearInterval(recordTimerInterval);
            recordBtn.classList.remove('recording');
            recordStatus.textContent = 'Đã ghi âm xong';
            recordTimer.classList.add('hidden');
            waveContainer.classList.add('hidden');
        }
    }

    function updateRecordTimer() {
        const diff = Date.now() - recordStartTime;
        const totalSecs = Math.floor(diff / 1000);
        const mins = String(Math.floor(totalSecs / 60)).padStart(2, '0');
        const secs = String(totalSecs % 60).padStart(2, '0');
        recordTimer.textContent = `${mins}:${secs}`;
    }

    // 4. File Drag and Drop / Input Selection
    dropZone.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    });

    function handleSelectedFile(file) {
        // Validate size (< 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showToast('Tệp quá lớn! Vui lòng tải file dưới 10MB.', 'error');
            return;
        }

        // Validate type
        if (!file.type.includes('audio') && !file.name.endsWith('.mp3') && !file.name.endsWith('.wav')) {
            showToast('Định dạng tệp không hợp lệ! Chỉ nhận .mp3 hoặc .wav.', 'error');
            return;
        }

        currentFile = file;
        fileNameDisplay.textContent = file.name;
        fileDetails.classList.remove('hidden');
        dropZone.classList.add('hidden');

        // Reset samples
        document.querySelectorAll('.sample-item').forEach(el => el.classList.remove('selected'));

        // Update Step 1 Status
        stepAudioBadge.textContent = 'Tệp tải lên';
        stepAudioBadge.className = 'step-badge badge-db';
        audioMetaInfo.innerHTML = `
            <p style="margin-bottom: 8px;"><strong>Tệp âm thanh:</strong> ${file.name}</p>
            <p style="margin-bottom: 8px; color: var(--text-muted); font-size: 11px;">Dung lượng: ${(file.size / 1024 / 1024).toFixed(2)} MB</p>
        `;

        recordedDuration = 0; // Reset for uploaded files
        const audioUrl = URL.createObjectURL(file);
        audioPlayer.src = audioUrl;
        audioPlayerContainer.classList.remove('hidden');

        // Highlight Step 1 as success
        resetPipelineVisuals();
        stepAudio.className = 'pipeline-step success';

        runPipelineBtn.removeAttribute('disabled');
        showToast('Nạp tệp âm thanh tải lên thành công!', 'success');
    }

    clearFileBtn.addEventListener('click', () => {
        clearFileInput();
        resetPipelineVisuals();
        showToast('Đã xóa tệp âm thanh.');
    });

    function clearFileInput() {
        currentFile = null;
        fileInput.value = '';
        fileDetails.classList.add('hidden');
        dropZone.classList.remove('hidden');
        runPipelineBtn.setAttribute('disabled', 'true');
        audioPlayerContainer.classList.add('hidden');
        audioPlayer.src = '';
        audioMetaInfo.innerHTML = '<p class="placeholder-text">Chưa nhận được âm thanh đầu vào.</p>';
        recordedDuration = 0;
        currentAudioDuration = 0;
        document.querySelectorAll('.sample-item').forEach(el => el.classList.remove('selected'));
    }

    // 5. Reset Visuals
    function resetPipelineVisuals() {
        ttsBtn.classList.add('hidden');
        if (currentTtsAudio) {
            currentTtsAudio.pause();
            currentTtsAudio = null;
        }
        ttsBtn.classList.remove('speaking');
        
        document.querySelectorAll('.pipeline-step').forEach(step => {
            step.className = 'pipeline-step';
        });
        
        // Hide badges inside headers
        document.querySelector('.badge-whisper').classList.add('hidden');
        document.querySelector('.badge-gemini').classList.add('hidden');
        document.querySelector('.badge-db').classList.add('hidden');

        // Clear details
        stepAsrDetails.innerHTML = '<p class="placeholder-text">Đang chờ âm thanh...</p>';
        stepLlmDetails.innerHTML = '<p class="placeholder-text">Đang chờ văn bản ASR...</p>';
        stepToolDetails.innerHTML = '<p class="placeholder-text">Đang chờ phân tích ý định...</p>';
        stepResponseDetails.innerHTML = '<p class="placeholder-text">Đang chờ câu trả lời hoàn thiện...</p>';
    }

    // 6. Run E2E Pipeline
    runPipelineBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        resetPipelineVisuals();
        runPipelineBtn.setAttribute('disabled', 'true');
        recordBtn.setAttribute('disabled', 'true');
        clearFileBtn.style.pointerEvents = 'none';

        try {
            // Pipeline Step 1: Input Audio
            stepAudio.className = 'pipeline-step success';
            showToast('Bắt đầu quy trình chạy E2E Pipeline...', 'info');

            // Pipeline Step 2: ASR (Processing)
            stepAsr.className = 'pipeline-step active processing';
            stepAsrDetails.innerHTML = `<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i> Mô hình Whisper đang dịch giọng nói tiếng Việt sang văn bản...</div>`;
            await delay(800); // UI visual transition

            // Prepare multipart form data
            const formData = new FormData();
            formData.append('file', currentFile);

            // Lấy ngôn ngữ nhận dạng ASR đã chọn
            const asrLangSelect = document.getElementById('asr-lang-select');
            const selectedLang = asrLangSelect ? asrLangSelect.value : 'vi';

            const startRequestTime = Date.now();
            const response = await fetch(`${API_URL}/chatbot/voice?language=${selectedLang}`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Lỗi xử lý pipeline trên server');
            }

            const data = await response.json();
            const pipeline = data.pipeline_results;
            const latency = ((Date.now() - startRequestTime) / 1000).toFixed(2);

            // Step 2 ASR (Success)
            const whisperBadge = document.querySelector('.badge-whisper');
            if (whisperBadge) {
                const modelName = data.whisper_model ? (data.whisper_model.charAt(0).toUpperCase() + data.whisper_model.slice(1)) : 'Tiny';
                whisperBadge.textContent = `Whisper ${modelName}`;
                whisperBadge.classList.remove('hidden');
            }
            stepAsr.className = 'pipeline-step success';
            stepAsrDetails.innerHTML = `
                <div class="chat-bubble" style="background: rgba(255,255,255,0.02); border-color: var(--border-color); margin-top:0;">
                    <strong>Văn bản nhận diện:</strong> "${pipeline.asr_transcript}"
                </div>
            `;
            showToast('Chuyển giọng nói sang chữ (ASR) thành công!', 'success');
            await delay(1000);

            // Step 3: LLM Intent & Entity (Processing)
            stepLlm.className = 'pipeline-step active processing';
            stepLlmDetails.innerHTML = `<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i> Gemini 3.1 Flash-Lite đang phân tích ý định và trích xuất thực thể...</div>`;
            await delay(800);

            // Step 3: LLM (Success)
            document.querySelector('.badge-gemini').classList.remove('hidden');
            stepLlm.className = 'pipeline-step success';
            
            const intentHtml = `<span class="intent-val"><i class="fa-solid fa-bullseye"></i> Intent: ${pipeline.intent}</span>`;
            let entitiesHtml = '';
            if (pipeline.tool_args && Object.keys(pipeline.tool_args).length > 0) {
                entitiesHtml = Object.entries(pipeline.tool_args).map(([k, v]) => {
                    return `<span class="entity-val"><strong>${k}:</strong> <span>${v}</span></span>`;
                }).join('');
            } else {
                entitiesHtml = `<span class="entity-val" style="color: var(--text-muted);">Không có thực thể</span>`;
            }

            stepLlmDetails.innerHTML = `
                <p>Mô hình LLM đã thực hiện trích xuất và Chain-of-Thought:</p>
                <div class="intent-display">
                    ${intentHtml}
                    ${entitiesHtml}
                </div>
            `;
            showToast('LLM phân tích ngữ nghĩa thành công!', 'success');
            await delay(1000);

            // Step 4: Tool Execution (Processing/Success)
            stepTool.className = 'pipeline-step active processing';
            stepToolDetails.innerHTML = `<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i> Đang gọi Mock API nghiệp vụ và truy vấn cơ sở dữ liệu...</div>`;
            await delay(800);

            document.querySelector('.badge-db').classList.remove('hidden');
            stepTool.className = 'pipeline-step success';
            
            if (pipeline.tool_called) {
                stepToolDetails.innerHTML = `
                    <p>Đã thực thi công cụ nghiệp vụ: <span class="tool-name-highlight">${pipeline.tool_called}()</span></p>
                    <p style="margin-top: 6px; font-size:12px;">Kết quả trả về từ Mock Database:</p>
                    <div class="json-display">${JSON.stringify(pipeline.tool_result, null, 2)}</div>
                `;
                showToast(`Thực thi tool ${pipeline.tool_called} thành công!`, 'success');
            } else {
                stepToolDetails.innerHTML = `
                    <p class="placeholder-text"><i class="fa-solid fa-circle-info"></i> Không cần gọi công cụ ngoại vi nào cho ý định này.</p>
                `;
            }
            await delay(1000);

            // Step 5: Final Response (Success)
            stepResponse.className = 'pipeline-step success';
            stepResponseDetails.innerHTML = `
                <div class="chat-bubble">${pipeline.agent_response}</div>
                <p style="font-size:11px; color: var(--text-muted); margin-top:8px; text-align:right;">
                    Phản hồi tự động trong ${latency} giây (Sử dụng ASR + LLM)
                </p>
            `;
            
            // Enable TTS Button & Voice Selector
            ttsBtn.classList.remove('hidden');
            ttsVoiceSelect.classList.remove('hidden');
            ttsBtn.onclick = () => speakText(pipeline.agent_response);
            
            showToast('Đã sinh câu trả lời chatbot cuối cùng!', 'success');
            
            // Play TTS response automatically
            speakText(pipeline.agent_response);

        } catch (err) {
            console.error(err);
            showToast(err.message || 'Có lỗi xảy ra trong quá trình chạy pipeline!', 'error');
            
            // Highlight current active step as failed
            const activeStep = document.querySelector('.pipeline-step.active');
            if (activeStep) {
                activeStep.className = 'pipeline-step';
                activeStep.querySelector('.step-details').innerHTML = `<p style="color: var(--danger);"><i class="fa-solid fa-circle-exclamation"></i> Lỗi: ${err.message}</p>`;
            }
        } finally {
            runPipelineBtn.removeAttribute('disabled');
            recordBtn.removeAttribute('disabled');
            clearFileBtn.style.pointerEvents = 'auto';
        }
    });

    // 7. TTS Voice Selection Helper
    function populateVoiceList() {
        ttsVoiceSelect.innerHTML = `
            <option value="vi-VN-HoaiMyNeural" selected>👩 Giọng Nữ - Hoài Mỹ (Edge Natural)</option>
            <option value="vi-VN-NamMinhNeural">👨 Giọng Nam - Nam Minh (Edge Natural)</option>
            <option value="en-US-AvaMultilingualNeural">👩 Giọng Nữ - Ava (Edge Multilingual)</option>
            <option value="en-US-AndrewMultilingualNeural">👨 Giọng Nam - Andrew (Edge Multilingual)</option>
        `;
        // Hiển thị dropdown ngay lập tức
        ttsVoiceSelect.classList.remove('hidden');
    }

    // 8. TTS (Speech Synthesis) Helper
    function speakText(text) {
        if (!text) return;
        
        // Stop current audio if playing
        if (currentTtsAudio) {
            currentTtsAudio.pause();
            currentTtsAudio = null;
        }

        const selectedVoice = ttsVoiceSelect.value;
        const ttsUrl = `${API_URL}/chatbot/tts?text=${encodeURIComponent(text)}&voice=${encodeURIComponent(selectedVoice)}`;
        
        currentTtsAudio = new Audio(ttsUrl);
        
        currentTtsAudio.onplay = () => {
            ttsBtn.classList.add('speaking');
            ttsBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Đang đọc...`;
        };

        currentTtsAudio.onended = () => {
            ttsBtn.classList.remove('speaking');
            ttsBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i> Nói`;
            currentTtsAudio = null;
        };

        currentTtsAudio.onerror = (e) => {
            console.error('Lỗi khi phát âm thanh TTS:', e);
            showToast('Không thể kết nối đến server để phát giọng nói Neural!', 'error');
            ttsBtn.classList.remove('speaking');
            ttsBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i> Nói`;
            currentTtsAudio = null;
        };

        currentTtsAudio.play().catch(err => {
            console.error('Không thể phát âm thanh:', err);
            showToast('Vui lòng cấp quyền phát âm thanh tự động trên trình duyệt!', 'warning');
            ttsBtn.classList.remove('speaking');
            ttsBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i> Nói`;
            currentTtsAudio = null;
        });
    }

    // Delay helper
    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Filters for Samples
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderSamples(btn.dataset.filter);
        });
    });

    // Custom Audio Player Listeners
    const playerPlayBtn = document.getElementById('player-play-btn');
    const playerMuteBtn = document.getElementById('player-mute-btn');
    const playerTimelineContainer = document.querySelector('.player-timeline-container');
    const playerProgress = document.getElementById('player-progress');
    const playerTime = document.getElementById('player-time');

    playerPlayBtn.addEventListener('click', () => {
        if (audioPlayer.paused) {
            audioPlayer.play().catch(err => {
                console.error("Playback error:", err);
                showToast("Không thể phát âm thanh này!", "error");
            });
        } else {
            audioPlayer.pause();
        }
    });

    playerMuteBtn.addEventListener('click', () => {
        audioPlayer.muted = !audioPlayer.muted;
        playerMuteBtn.innerHTML = audioPlayer.muted ? 
            '<i class="fa-solid fa-volume-xmark"></i>' : 
            '<i class="fa-solid fa-volume-high"></i>';
    });

    audioPlayer.addEventListener('play', () => {
        playerPlayBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
    });

    audioPlayer.addEventListener('pause', () => {
        playerPlayBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
    });

    audioPlayer.addEventListener('ended', () => {
        playerPlayBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        playerProgress.style.width = '0%';
    });

    audioPlayer.addEventListener('timeupdate', () => {
        const current = audioPlayer.currentTime;
        const duration = currentAudioDuration || audioPlayer.duration || 0;
        const percent = (isFinite(duration) && duration > 0) ? (current / duration) * 100 : 0;
        playerProgress.style.width = `${percent}%`;
        playerTime.textContent = `${formatTime(current)} / ${formatTime(duration)}`;
    });

    audioPlayer.addEventListener('loadedmetadata', () => {
        const duration = audioPlayer.duration;
        if (isFinite(duration) && duration > 0) {
            currentAudioDuration = duration;
        } else if (recordedDuration > 0) {
            currentAudioDuration = recordedDuration;
        } else {
            currentAudioDuration = 0;
        }
        playerTime.textContent = `00:00 / ${formatTime(currentAudioDuration)}`;
    });

    playerTimelineContainer.addEventListener('click', (e) => {
        const rect = playerTimelineContainer.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const width = rect.width;
        const duration = currentAudioDuration || audioPlayer.duration || 0;
        if (width > 0 && duration > 0 && isFinite(duration)) {
            audioPlayer.currentTime = (clickX / width) * duration;
        }
    });

    function formatTime(secs) {
        if (isNaN(secs)) return '00:00';
        const m = String(Math.floor(secs / 60)).padStart(2, '0');
        const s = String(Math.floor(secs % 60)).padStart(2, '0');
        return `${m}:${s}`;
    }

    // Initialize list of voices
    populateVoiceList();

    // Bootstrap loading
    loadSamples();
});
