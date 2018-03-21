var ls;
(function (ls) {
    var AISpriteSheet = (function (_super) {
        __extends(AISpriteSheet, _super);
        function AISpriteSheet() {
            _super.call(this);
            this.loop = Number.MAX_VALUE;
            this.frameRate = 4;
            this.speedRate = 1;
            this.cacheTexutres = {};
            this._currentloop = 0;
            this._currentFrame = 0;
            this._isPlaying = true;
            this.isFirstPlay = true;
            this.name = "spritesheet";
            this.container.addChild(this._bitmap);
        }
        var d = __define,c=AISpriteSheet,p=c.prototype;
        p.initialize = function () {
            this.url = ls.eval_e(decodeURIComponent(this["url"]));
            this.segmentH = ls.eval_e(decodeURIComponent(this["segmentH"]));
            this.segmentV = ls.eval_e(decodeURIComponent(this["segmentV"]));
            this.loop = ls.eval_e(decodeURIComponent(this["loop"]));
            this.defaultStart = ls.eval_e(decodeURIComponent(this["defaultStart"]));
            this.frameRate = ls.eval_e(decodeURIComponent(this["frameRate"]));
            this.speedRate = ls.eval_e(decodeURIComponent(this["speedRate"]));
            if (this.segmentH < 1)
                this.segmentH = 1;
            if (this.segmentV < 1)
                this.segmentV = 1;
            if (isNaN(this.loop))
                this.loop = Number.MAX_VALUE;
            if (this.loop <= 0)
                this.loop = Number.MAX_VALUE;
            if (isNaN(this.frameRate))
                this.frameRate = 5;
            if (this.frameRate < 0)
                this.frameRate = 0.0001;
            var textureDatas = ls.getTexture(this.url);
            if (textureDatas != null)
                this.texture = textureDatas[0];
            if (this.texture)
                this.onResourceLoadComplete();
            else {
                RES.getResByUrl(this.url, function (texture) {
                    this.texture = texture;
                    this.onResourceLoadComplete();
                }, this, RES.ResourceItem.TYPE_IMAGE);
            }
        };
        p.onTick = function () {
            if (!this.isCacheComplete)
                return;
            if (this._currentloop >= this.loop)
                return;
            if (!this.defaultStart && !this.isFirstPlay)
                return;
            this._currentFrame = this._currentFrame % this._totalFrames;
            var currentTime = egret.getTimer();
            if (this.isFirstPlay || (!this.isFirstPlay && currentTime - this._oldTime >= this.duration / this.speedRate)) {
                this.isFirstPlay = false;
                this._bitmap.texture = this.cacheTexutres[this._currentFrame];
                this._oldTime = currentTime;
                if (this._isPlaying) {
                    if (this._currentFrame < this._totalFrames) {
                        this._currentFrame++;
                        if (this._currentFrame == this._totalFrames)
                            this.dispatchEvent(new ls.TriggerEvent(ls.TriggerEvent.TRIGGER, this.onSpriteSheetPlayComplete));
                    }
                    else {
                        this._currentFrame = 1;
                        this._currentloop++;
                    }
                }
                if (this._currentloop == this.loop) {
                    this._isPlaying = false;
                    this.dispatchEvent(new ls.TriggerEvent(ls.TriggerEvent.TRIGGER, this.onSpriteSheetAllPlayComplete));
                }
            }
        };
        p.onResourceLoadComplete = function () {
            this.spritesheet = new egret.SpriteSheet(this.texture);
            this.canvasWidth = Math.ceil(this.texture.textureWidth / this.segmentH);
            this.canvasHeight = Math.ceil(this.texture.textureHeight / this.segmentV);
            var nums = 0;
            for (var i = 0; i < this.segmentV; i++) {
                for (var j = 0; j < this.segmentH; j++) {
                    var renderTexture = this.spritesheet.createTexture(nums.toString(), this.canvasWidth * j, this.canvasHeight * i, this.canvasWidth, this.canvasHeight, 0, 0, this.texture.textureWidth, this.texture.textureHeight);
                    this.cacheTexutres[nums.toString()] = renderTexture;
                    nums++;
                }
            }
            this.duration = 1000 / this.frameRate;
            this._totalFrames = nums;
            this.isCacheComplete = true;
        };
        p.onSpriteSheetAllPlayComplete = function ($onAllPlayComplete) {
            return { instances: [this], status: true };
        };
        p.onSpriteSheetPlayComplete = function ($onPlayComplete) {
            return { instances: [this], status: true };
        };
        p.isPlayingCheck = function ($isPlaying) {
            return { instances: [this], status: this._isPlaying };
        };
        p.compareFrame = function ($event) {
            return { instances: [this], status: ls.compare(this._currentFrame, $event.operationType, $event.frame) };
        };
        p.compareSpeed = function ($event) {
            return { instances: [this], status: ls.compare(this.speedRate, $event.operationType, $event.speed) };
        };
        p.compareLoop = function ($event) {
            return { instances: [this], status: ls.compare(this.loop, $event.operationType, $event.loop) };
        };
        p.gotoAndPlay = function (frame, loop) {
            this._currentloop = 0;
            var frame = ls.eval_e(frame);
            var loop = ls.eval_e(loop);
            ls.assert(typeof frame !== "number" || typeof loop !== "number", "AIMovieClip gotoAndPlay parameter type incorrect!!");
            this._currentFrame = frame;
            this.loop = loop;
            this._isPlaying = true;
        };
        p.gotoAndStop = function (frame) {
            this._currentloop = 0;
            var frame = ls.eval_e(frame);
            ls.assert(typeof frame !== "number", "AIMovieClip gotoAndStop parameter type incorrect!!");
            this._currentFrame = frame;
            this._isPlaying = false;
        };
        p.play = function (loop) {
            this._currentloop = 0;
            var loop = ls.eval_e(loop);
            ls.assert(typeof loop !== "number", "AIMovieClip play parameter type incorrect!!");
            this.loop = (loop <= 0 ? Number.MAX_VALUE : loop);
            this._isPlaying = true;
        };
        p.stop = function () {
            this._currentloop = 0;
            this._isPlaying = false;
        };
        p.prevFrame = function () {
            this._currentloop = 0;
            if (this._currentFrame > 1)
                this._currentFrame--;
            this._isPlaying = false;
        };
        p.nextFrame = function () {
            this._currentloop = 0;
            if (this._currentFrame < this._totalFrames)
                this._currentFrame++;
            this._isPlaying = false;
        };
        p.setLoop = function (loop) {
            var loop = ls.eval_e(loop);
            ls.assert(typeof loop !== "number", "AIMovieClip setLoop parameter type incorrect!!");
            this.loop = loop;
        };
        p.setSpeedRate = function (speedRate) {
            var speedRate = ls.eval_e(speedRate);
            ls.assert(typeof speedRate !== "number", "AIMovieClip setSpeedRate parameter type incorrect!!");
            this.speedRate = speedRate || 1;
            if (this.speedRate <= 0)
                this.speedRate = 0.000001;
        };
        d(p, "totalFrames"
            ,function () {
                return this._totalFrames;
            }
        );
        d(p, "currentFrame"
            ,function () {
                return this._currentFrame;
            }
        );
        d(p, "isPlaying"
            ,function () {
                return this._isPlaying;
            }
        );
        p.saveToJSON = function () {
            var o = _super.prototype.saveToJSON.call(this);
            o.url = this.url;
            o.segmentH = this.segmentH;
            o.segmentV = this.segmentV;
            o.loop = this.loop;
            o.defaultStart = this.defaultStart;
            o.frameRate = this.frameRate;
            o.speedRate = this.speedRate;
            return o;
        };
        p.loadFromJSON = function (o) {
            if (o) {
                _super.prototype.loadFromJSON.call(this, o);
                this.url = o.url;
                this.segmentH = o.segmentH;
                this.segmentV = o.segmentV;
                this.loop = o.loop;
                this.defaultStart = o.defaultStart;
                this.frameRate = o.frameRate;
                this.speedRate = o.speedRate;
            }
        };
        p.clone = function () {
            var cl = _super.prototype.clone.call(this);
            cl.url = this.url;
            cl.segmentH = this.segmentH;
            cl.segmentV = this.segmentV;
            cl.loop = this.loop;
            cl.defaultStart = this.defaultStart;
            cl.frameRate = this.frameRate;
            cl.speedRate = this.speedRate;
            return cl;
        };
        return AISpriteSheet;
    }(ls.AISprite));
    ls.AISpriteSheet = AISpriteSheet;
    egret.registerClass(AISpriteSheet,'ls.AISpriteSheet');
    var OnSpriteSheetAllPlayCompleteEvent = (function (_super) {
        __extends(OnSpriteSheetAllPlayCompleteEvent, _super);
        function OnSpriteSheetAllPlayCompleteEvent() {
            _super.call(this);
        }
        var d = __define,c=OnSpriteSheetAllPlayCompleteEvent,p=c.prototype;
        return OnSpriteSheetAllPlayCompleteEvent;
    }(ls.BaseEvent));
    ls.OnSpriteSheetAllPlayCompleteEvent = OnSpriteSheetAllPlayCompleteEvent;
    egret.registerClass(OnSpriteSheetAllPlayCompleteEvent,'ls.OnSpriteSheetAllPlayCompleteEvent');
    var OnSpriteSheetPlayCompleteEvent = (function (_super) {
        __extends(OnSpriteSheetPlayCompleteEvent, _super);
        function OnSpriteSheetPlayCompleteEvent() {
            _super.call(this);
        }
        var d = __define,c=OnSpriteSheetPlayCompleteEvent,p=c.prototype;
        return OnSpriteSheetPlayCompleteEvent;
    }(ls.BaseEvent));
    ls.OnSpriteSheetPlayCompleteEvent = OnSpriteSheetPlayCompleteEvent;
    egret.registerClass(OnSpriteSheetPlayCompleteEvent,'ls.OnSpriteSheetPlayCompleteEvent');
    var IsSpriteSheetPlayingEvent = (function (_super) {
        __extends(IsSpriteSheetPlayingEvent, _super);
        function IsSpriteSheetPlayingEvent() {
            _super.call(this);
        }
        var d = __define,c=IsSpriteSheetPlayingEvent,p=c.prototype;
        return IsSpriteSheetPlayingEvent;
    }(ls.BaseEvent));
    ls.IsSpriteSheetPlayingEvent = IsSpriteSheetPlayingEvent;
    egret.registerClass(IsSpriteSheetPlayingEvent,'ls.IsSpriteSheetPlayingEvent');
    var CompareSpriteSheetFrameEvent = (function (_super) {
        __extends(CompareSpriteSheetFrameEvent, _super);
        function CompareSpriteSheetFrameEvent() {
            _super.call(this);
        }
        var d = __define,c=CompareSpriteSheetFrameEvent,p=c.prototype;
        return CompareSpriteSheetFrameEvent;
    }(ls.BaseEvent));
    ls.CompareSpriteSheetFrameEvent = CompareSpriteSheetFrameEvent;
    egret.registerClass(CompareSpriteSheetFrameEvent,'ls.CompareSpriteSheetFrameEvent');
    var CompareSpriteSheetSpeedEvent = (function (_super) {
        __extends(CompareSpriteSheetSpeedEvent, _super);
        function CompareSpriteSheetSpeedEvent() {
            _super.call(this);
        }
        var d = __define,c=CompareSpriteSheetSpeedEvent,p=c.prototype;
        return CompareSpriteSheetSpeedEvent;
    }(ls.BaseEvent));
    ls.CompareSpriteSheetSpeedEvent = CompareSpriteSheetSpeedEvent;
    egret.registerClass(CompareSpriteSheetSpeedEvent,'ls.CompareSpriteSheetSpeedEvent');
    var CompareSpriteSheetLoopEvent = (function (_super) {
        __extends(CompareSpriteSheetLoopEvent, _super);
        function CompareSpriteSheetLoopEvent() {
            _super.call(this);
        }
        var d = __define,c=CompareSpriteSheetLoopEvent,p=c.prototype;
        return CompareSpriteSheetLoopEvent;
    }(ls.BaseEvent));
    ls.CompareSpriteSheetLoopEvent = CompareSpriteSheetLoopEvent;
    egret.registerClass(CompareSpriteSheetLoopEvent,'ls.CompareSpriteSheetLoopEvent');
})(ls || (ls = {}));
