"""
Fontra backend integration for feamerge plugin
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Callable, Optional

from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib2 import Font

from .combine_features import VariableFeatureCombiner
from .break_groups_in_fea import expand_kerning_groups
from .break_groups_in_mark_pos import expand_mark_positioning_groups

logger = logging.getLogger(__name__)


class FeamergeBackend:
    """
    Backend for the Feamerge Fontra plugin.
    
    Handles feature file merging and group expansion operations
    on designspace files and their UFO sources.
    """

    @classmethod
    def fromPath(cls, path: Path):
        """Create a backend instance from a file path."""
        return cls(path)

    def __init__(self, path: Path):
        """
        Initialize the backend.
        
        Args:
            path: Path to the designspace file
        """
        self.path = Path(path)
        self.designspace = None
        self.combiner = None
        self._load_designspace()

    def _load_designspace(self):
        """Load the designspace file."""
        if not self.path.exists():
            raise FileNotFoundError(f"Designspace file not found: {self.path}")
        
        if not self.path.suffix == ".designspace":
            raise ValueError(f"Expected .designspace file, got: {self.path.suffix}")
        
        self.designspace = DesignSpaceDocument.fromfile(self.path)
        self.combiner = VariableFeatureCombiner(str(self.path))
        logger.info(f"Loaded designspace: {self.path}")

    async def mergeFeatures(
        self, 
        output_path: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Merge all feature files from designspace sources into variable feature syntax.
        
        Args:
            output_path: Optional custom output path for merged features
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with status and output path
        """
        try:
            if progress_callback:
                await progress_callback(0.1, "Initializing feature merge...")
            
            loop = asyncio.get_event_loop()
            
            if progress_callback:
                await progress_callback(0.3, "Combining features...")
            
            output_file = output_path or "variable_features.fea"
            output_path = self.path.parent / output_file
            
            await loop.run_in_executor(
                None,
                self.combiner.save_combined_features,
                str(output_path)
            )
            
            if progress_callback:
                await progress_callback(1.0, "Feature merge complete!")
            
            logger.info(f"Features merged successfully: {output_path}")
            
            return {
                "status": "success",
                "message": f"Features merged to {output_file}",
                "output_path": str(output_path),
            }
            
        except Exception as e:
            logger.error(f"Error merging features: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Error merging features: {str(e)}",
            }

    async def breakKerningGroups(
        self,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Break kerning groups in all UFO sources.
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with status and processed sources
        """
        try:
            sources = self.designspace.sources
            total = len(sources)
            processed = []
            
            if progress_callback:
                await progress_callback(0, "Starting kerning group expansion...")
            
            loop = asyncio.get_event_loop()
            
            for i, source in enumerate(sources):
                ufo_path = self.path.parent / source.path
                
                if progress_callback:
                    await progress_callback(
                        i / total,
                        f"Processing {source.filename}..."
                    )
                
                await loop.run_in_executor(
                    None,
                    expand_kerning_groups,
                    str(ufo_path)
                )
                
                processed.append(source.filename)
                logger.info(f"Expanded kerning groups in: {source.filename}")
            
            if progress_callback:
                await progress_callback(1.0, "All kerning groups expanded!")
            
            return {
                "status": "success",
                "message": f"Kerning groups expanded in {len(processed)} sources",
                "processed": processed,
            }
            
        except Exception as e:
            logger.error(f"Error breaking kerning groups: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Error breaking kerning groups: {str(e)}",
            }

    async def breakMarkGroups(
        self,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Break mark positioning groups in all UFO sources.
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with status and processed sources
        """
        try:
            sources = self.designspace.sources
            total = len(sources)
            processed = []
            
            if progress_callback:
                await progress_callback(0, "Starting mark positioning group expansion...")
            
            loop = asyncio.get_event_loop()
            
            for i, source in enumerate(sources):
                ufo_path = self.path.parent / source.path
                
                if progress_callback:
                    await progress_callback(
                        i / total,
                        f"Processing {source.filename}..."
                    )
                
                await loop.run_in_executor(
                    None,
                    expand_mark_positioning_groups,
                    str(ufo_path)
                )
                
                processed.append(source.filename)
                logger.info(f"Expanded mark groups in: {source.filename}")
            
            if progress_callback:
                await progress_callback(1.0, "All mark positioning groups expanded!")
            
            return {
                "status": "success",
                "message": f"Mark positioning groups expanded in {len(processed)} sources",
                "processed": processed,
            }
            
        except Exception as e:
            logger.error(f"Error breaking mark groups: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Error breaking mark groups: {str(e)}",
            }

    async def processAll(
        self,
        output_path: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Process all operations: break groups and merge features.
        
        Args:
            output_path: Optional custom output path for merged features
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with combined status
        """
        try:
            results = {}
            
            if progress_callback:
                await progress_callback(0, "Step 1/3: Breaking kerning groups...")
            
            kerning_result = await self.breakKerningGroups(progress_callback)
            results["kerning"] = kerning_result
            
            if kerning_result["status"] == "error":
                return kerning_result
            
            if progress_callback:
                await progress_callback(0.33, "Step 2/3: Breaking mark positioning groups...")
            
            mark_result = await self.breakMarkGroups(progress_callback)
            results["mark"] = mark_result
            
            if mark_result["status"] == "error":
                return mark_result
            
            if progress_callback:
                await progress_callback(0.66, "Step 3/3: Merging features...")
            
            merge_result = await self.mergeFeatures(output_path, progress_callback)
            results["merge"] = merge_result
            
            if merge_result["status"] == "error":
                return merge_result
            
            if progress_callback:
                await progress_callback(1.0, "All processing complete!")
            
            return {
                "status": "success",
                "message": "All operations completed successfully",
                "results": results,
            }
            
        except Exception as e:
            logger.error(f"Error in processAll: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Error in processAll: {str(e)}",
            }

